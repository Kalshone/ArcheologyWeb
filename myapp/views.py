from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.db.utils import IntegrityError
from .models import Site, Sites, Areas, Artifacts
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, get_object_or_404
from django.apps import apps
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlencode
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Group
from .models import EditorTablePermission
from .forms import EditorTablePermissionForm
from django.core.paginator import Paginator
import csv
from django.contrib.auth.decorators import login_required
import json

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def manage_editor_permissions(request):
    editors = User.objects.filter(groups__name='Editor')
    tables = ['Sites']  # Add your table names here
    
    if request.method == 'POST':
        editor_id = request.POST.get('editor')
        table_name = request.POST.get('table')
        editor = User.objects.get(id=editor_id)
        
        permission, created = EditorTablePermission.objects.get_or_create(
            editor=editor,
            table_name=table_name
        )
        
        form = EditorTablePermissionForm(request.POST, instance=permission)
        if form.is_valid():
            form.save()
    
    permissions = EditorTablePermission.objects.all()
    form = EditorTablePermissionForm()
    
    return render(request, 'manage_permissions.html', {
        'editors': editors,
        'tables': tables,
        'permissions': permissions,
        'form': form
    })

def landing_page(request):
    # Render the landing page template
    return render(request, 'landing.html')

# def login(request):
#     # Redirect to the dashboard view
#     return redirect('dashboard')

from .forms import EditorSignUpForm
from .models import EditorRegistrationCode

def signup(request):
    if request.method == 'POST':
        form = EditorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Add user to editor group
            editor_group, created = Group.objects.get_or_create(name='Editor')
            user.groups.add(editor_group)
            # Mark registration code as used
            code = form.cleaned_data.get('editor_code')
            registration_code = EditorRegistrationCode.objects.get(code=code)
            registration_code.is_used = True
            registration_code.save()
            messages.success(request, 'Editor account created successfully!')
            return redirect('login')
    else:
        form = EditorSignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def login(request):
    return render(request, 'registration/login.html')

def dashboard(request):
    """Guest access allowed - read-only"""
    # Count actual data from the Sites model
    sites_count = Sites.objects.count()
    areas_count = Areas.objects.count()
    artifacts_count = Artifacts.objects.count()
    
    # Get the most recently modified site (if any exist)
    recent_site = Sites.objects.order_by('siteNo').first()
    
    can_edit = request.user.is_authenticated and (
        request.user.is_superuser or 
        request.user.groups.filter(name='Editor').exists()
    )
    
    return render(request, 'home.html', {
        'sites_count': sites_count,
        'areas_count': areas_count,
        'artifacts_count': artifacts_count,
        'recent_site': recent_site,
        'can_edit': can_edit
    })

# def sites(request):
#     if request.method == 'POST':
#         site_data = {field: request.POST[field] for field in request.POST if field != 'csrfmiddlewaretoken'}
#         try:
#             site = Site.objects.create(**site_data)
#             return JsonResponse({'success': True})
#         except IntegrityError:
#             return JsonResponse({'success': False, 'error': "A site with this number already exists."})
    
#     sites = Site.objects.all()
#     headers = [{
#         'name': field.name,
#         'verbose_name': field.verbose_name,
#         'is_primary_key': field.primary_key,
#         'type': field.get_internal_type()
#     } for field in Site._meta.fields]
#     return render(request, 'sites.html', {
#         'sites': sites, 
#         'headers': headers,
#         'model_name': 'Site'
#     })


def table_view(request, model_name):
    if 'icon' in model_name.lower() or model_name.lower() == 'favicon.ico':
        return HttpResponse(status=204)  # Return empty response
    try:
        model = apps.get_model(app_label='myapp', model_name=model_name)
    except LookupError:
        raise Http404(f"Model '{model_name}' does not exist")
    
    pk_field = model._meta.pk.name
    objects = model.objects.all().order_by(pk_field)
    
    page_size = int(request.GET.get('size', 10))
    page_size = min(max(page_size, 10), 100)
    
    can_add = False
    can_edit = False
    can_delete = False

    if request.user.is_authenticated:
        if request.user.is_superuser:
            can_add = True
            can_edit = True
            can_delete = True
        elif request.user.groups.filter(name='Editor').exists():
            try:
                perm = EditorTablePermission.objects.get(
                    editor=request.user,
                    table_name=model_name
                )
                can_add = perm.can_add
                can_edit = perm.can_edit
                can_delete = perm.can_delete
            except EditorTablePermission.DoesNotExist:
                pass
            
    paginator = Paginator(objects, page_size)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.method == 'POST':
        object_data = {field: request.POST[field] for field in request.POST if field != 'csrfmiddlewaretoken'}
        
        # Process foreign keys
        for field in model._meta.fields:
            if field.__class__.__name__ == 'ForeignKey' and field.name in object_data:
                # Get the related model
                related_model = field.remote_field.model
                # Get the object from the related model
                try:
                    related_obj = related_model.objects.get(pk=object_data[field.name])
                    object_data[field.name] = related_obj
                except related_model.DoesNotExist:
                    return JsonResponse({
                        'success': False, 
                        'error': f"Related {field.verbose_name} with id {object_data[field.name]} does not exist."
                    })
        
        try:
            obj = model.objects.create(**object_data)
            return JsonResponse({'success': True})
        except IntegrityError:
            return JsonResponse({'success': False, 'error': f"A {model_name} with this ID already exists."})
    
    headers = []
    for field in model._meta.fields:
        field_info = {
            'name': field.name,
            'verbose_name': field.verbose_name,
            'is_primary_key': field.primary_key,
            'type': field.__class__.__name__,
            'required': not field.blank and not field.primary_key,
            'max_length': getattr(field, 'max_length', None),
            'max_digits': getattr(field, 'max_digits', None),
            'decimal_places': getattr(field, 'decimal_places', None),
            'choices': [{'value': choice[0], 'display': choice[1]} for choice in field.choices] if field.choices else None
        }
        
        # Add related objects for ForeignKey fields
        if field.__class__.__name__ == 'ForeignKey':
            related_model = field.remote_field.model
            field_info['related_objects'] = related_model.objects.all()
        
        headers.append(field_info)
    
    return render(request, 'table_view.html', {
        'objects':  page_obj,
        'headers': headers,
        'model_name': model_name,
        'can_add': can_add,
        'can_edit': can_edit,
        'can_delete': can_delete,
        'page_obj': page_obj,
        'is_editor': request.user.is_authenticated and request.user.groups.filter(name='Editor').exists(),
        'is_admin': request.user.is_authenticated and request.user.is_superuser,
        'page_size': page_size,
    })
    
@csrf_exempt
def delete_object(request, model_name, object_id):
    if request.method == 'POST':
        try:
            # Convert the first character to uppercase (Site instead of site)
            model_name_capitalized = model_name.capitalize()
            model = apps.get_model(app_label='myapp', model_name=model_name_capitalized)
            # Dynamically get the primary key field name
            pk_field = model._meta.pk.name
            
            # Debug information
            print(f"Trying to delete {model_name_capitalized} with {pk_field}={object_id}")
            
            obj = get_object_or_404(model, **{pk_field: object_id})
            obj.delete()
            
            return JsonResponse({'success': True})
        except Exception as e:
            print(f"Error deleting object: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

import json
from django.views.decorators.http import require_POST

@require_POST
@csrf_exempt
def update_object(request, model_name, object_id):
    try:
        # Important: Use the exact model name as registered in Django
        # If URL has "sites" but model is "Site", we need to handle this
        model_name_exact = model_name.capitalize() if model_name.lower() != model_name else model_name
        
        # Debug logging
        print(f"Trying to update {model_name_exact} with id {object_id}")
        
        model = apps.get_model(app_label='myapp', model_name=model_name_exact)
        obj = model.objects.get(pk=object_id)
        
        data = json.loads(request.body)
        updated_fields = []
        
        # Create mappings for field names with different variations
        field_mapping = {}
        for field in model._meta.fields:
            # Map verbose_name, actual name, and lowercase versions
            field_mapping[field.verbose_name.lower()] = field.name
            field_mapping[field.name.lower()] = field.name
            # Also map without spaces and special characters
            clean_name = field.verbose_name.lower().replace(' ', '').replace('_', '')
            field_mapping[clean_name] = field.name
        
        # Also add the primary key field with different variations
        pk_field = model._meta.pk.name
        field_mapping[pk_field.lower()] = pk_field
        field_mapping['id'] = pk_field
        field_mapping['pk'] = pk_field
        
        print(f"Field mapping: {field_mapping}")
        
        for key, value in data.items():
            if key.startswith('field'):
                # Extract the field name by removing 'field' prefix
                field_name = key[5:].lower()  # Convert to lowercase for case-insensitive matching
                field_name_clean = field_name.replace(' ', '').replace('_', '')
                
                print(f"Looking for field: {field_name}")
                
                # Find the matching field in the model using our mapping
                actual_field_name = None
                if field_name in field_mapping:
                    actual_field_name = field_mapping[field_name]
                elif field_name_clean in field_mapping:
                    actual_field_name = field_mapping[field_name_clean]
                
                if actual_field_name:
                    # Skip the primary key field if we're trying to update it
                    if actual_field_name == pk_field:
                        print(f"Skipping primary key field: {actual_field_name}")
                        continue
                    
                    print(f"Matched field {field_name} to {actual_field_name}")
                    setattr(obj, actual_field_name, value)
                    updated_fields.append(actual_field_name)
                else:
                    print(f"Field not found: {field_name}")
                    print(f"Available fields: {list(field_mapping.keys())}")
        
        if updated_fields:
            obj.save(update_fields=updated_fields)
            
        return JsonResponse({
            'success': True, 
            'updated_fields': updated_fields,
            'message': f'Updated {model_name} {object_id} successfully'
        })
    except model.DoesNotExist:
        print(f"Object not found: {model_name} {object_id}")
        return JsonResponse({
            'success': False, 
            'error': f'Object {model_name} with ID {object_id} not found'
        }, status=404)
    except Exception as e:
        print(f"Error updating object: {str(e)}")
        return JsonResponse({
            'success': False, 
            'error': str(e)
        }, status=400)

def export_table(request, model_name):
    # Get the model
    model = apps.get_model(app_label='myapp', model_name=model_name)
    
    # Get all objects
    objects = model.objects.all()
    
    # Apply search filter if provided
    search_filter = request.POST.get('search_filter', '')
    if search_filter:
        # Create a Q object for each field to search
        from django.db.models import Q
        q_objects = Q()
        
        # Add each field to the search
        for field in model._meta.fields:
            # Only search text-based fields
            if field.__class__.__name__ in ['CharField', 'TextField']:
                q_objects |= Q(**{f"{field.name}__icontains": search_filter})
        
        # Apply the filter if we have any valid fields
        if q_objects:
            objects = objects.filter(q_objects)
    
    # Create the HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{model_name}.csv"'
    
    # Create CSV writer
    writer = csv.writer(response)
    
    # Write headers
    headers = [field.verbose_name for field in model._meta.fields]
    writer.writerow(headers)
    
    # Write data rows
    for obj in objects:
        row = []
        for field in model._meta.fields:
            value = getattr(obj, field.name)
            # Handle special cases like ForeignKey
            if field.__class__.__name__ == 'ForeignKey' and value is not None:
                value = str(value)
            if field.choices and value:
                # Get the display value for choice fields
                value = dict(field.choices).get(value, value)
            row.append(value)
        writer.writerow(row)
    
    return response


import csv
import io
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# Templates export (for import)
@login_required
def export_template(request, model_name):
    # Get the model
    model = apps.get_model(app_label='myapp', model_name=model_name)
    
    # Create the HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{model_name}_template.csv"'
    
    # Create CSV writer
    writer = csv.writer(response)
    
    # Write only headers (no data)
    headers = [field.verbose_name for field in model._meta.fields]
    writer.writerow(headers)
    
    return response

@login_required
@require_POST
def import_csv(request):
    if request.method == 'POST':
        try:
            # Get the model name from the form data
            model_name = request.POST.get('model_name')
            if not model_name:
                return JsonResponse({'success': False, 'error': 'Model name not provided'})
            
            # Get the model class
            try:
                model = apps.get_model(app_label='myapp', model_name=model_name)
            except LookupError:
                return JsonResponse({'success': False, 'error': f'Model {model_name} not found'})
            
            # Get the file and import mode
            file = request.FILES.get('csvFile')
            if not file:
                return JsonResponse({'success': False, 'error': 'No file provided'})
            
            import_mode = request.POST.get('importMode', 'both')
            has_header = request.POST.get('headerRow', 'on') == 'on'
            
            # Process the CSV file
            created = 0
            updated = 0
            errors = 0
            error_messages = []
            
            # Read CSV file
            decoded_file = file.read().decode('utf-8').splitlines()
            
            # Get field mappings - map CSV headers to model fields
            field_mapping = {}
            pk_field = model._meta.pk.name
            
            # Create field type mapping to handle type conversions
            field_types = {}
            
            for field in model._meta.fields:
                # Map verbose_name, actual name, and lowercase versions
                field_mapping[field.verbose_name.lower()] = field.name
                field_mapping[field.name.lower()] = field.name
                # Also map without spaces and special characters
                clean_name = field.verbose_name.lower().replace(' ', '').replace('_', '')
                field_mapping[clean_name] = field.name
                
                # Store field type information
                field_types[field.name] = field.__class__.__name__
            
            # Process rows
            if has_header:
                # Process with headers (DictReader)
                reader = csv.DictReader(decoded_file)
                for row in reader:
                    try:
                        # Convert keys to match our model fields
                        processed_row = {}
                        
                        for key, value in row.items():
                            key_lower = key.lower()
                            key_clean = key_lower.replace(' ', '').replace('_', '')
                            
                            # Find the matching field
                            actual_field = None
                            if key_lower in field_mapping:
                                actual_field = field_mapping[key_lower]
                            elif key_clean in field_mapping:
                                actual_field = field_mapping[key_clean]
                            
                            if actual_field:
                                # Skip empty values for numeric fields
                                if value == "" and field_types.get(actual_field) in [
                                    'DecimalField', 'FloatField', 'IntegerField', 
                                    'PositiveIntegerField', 'BigIntegerField'
                                ]:
                                    continue
                                
                                processed_row[actual_field] = value
                        
                        # Process the row based on import mode
                        if import_mode in ['create', 'both']:
                            # Handle foreign keys
                            for field in model._meta.fields:
                                if field.__class__.__name__ == 'ForeignKey' and field.name in processed_row:
                                    value = processed_row[field.name]
                                    if value:
                                        try:
                                            # Get the related model
                                            related_model = field.remote_field.model
                                            # Find object by primary key
                                            related_obj = related_model.objects.get(pk=value)
                                            processed_row[field.name] = related_obj
                                        except related_model.DoesNotExist:
                                            # Skip this field if the related object doesn't exist
                                            del processed_row[field.name]
                            
                            # Create new object
                            if import_mode == 'create' or not model.objects.filter(pk=processed_row.get(pk_field, '')).exists():
                                model.objects.create(**processed_row)
                                created += 1
                            # Update existing object
                            elif import_mode in ['update', 'both'] and pk_field in processed_row:
                                pk_value = processed_row.pop(pk_field, None)  # Remove PK from update dict
                                if pk_value:
                                    model.objects.filter(pk=pk_value).update(**processed_row)
                                    updated += 1
                    except Exception as e:
                        errors += 1
                        print(f"Error importing row: {e}")
            else:
                # Process without headers
                reader = csv.reader(decoded_file)
                field_names = [field.name for field in model._meta.fields]
                
                for row in reader:
                    try:
                        if len(row) > len(field_names):
                            row = row[:len(field_names)]  # Truncate if too many columns
                        elif len(row) < len(field_names):
                            row = row + [""] * (len(field_names) - len(row))  # Pad if too few
                        
                        processed_row = dict(zip(field_names, row))
                        
                        # Handle import based on mode (similar to above)
                        # Handle foreign keys and create/update logic would go here,
                        # similar to the code in the has_header block
                        
                        if import_mode in ['create', 'both']:
                            model.objects.create(**processed_row)
                            created += 1
                    except Exception as e:
                        errors += 1
                        print(f"Error importing row: {e}")
            
            return JsonResponse({
                'success': True,
                'created': created,
                'updated': updated,
                'errors': errors
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})