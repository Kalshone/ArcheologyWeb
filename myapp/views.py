from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.utils import IntegrityError
from .models import Site
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
import json

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def manage_editor_permissions(request):
    editors = User.objects.filter(groups__name='Editor')
    tables = ['Site']  # Add your table names here
    
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

# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Account created successfully! Please log in.')
#             return redirect('login')
#     else:
#         form = UserCreationForm()
#     return render(request, 'registration/signup.html', {'form': form})

def dashboard(request):
    """Guest access allowed - read-only"""
    sites = Site.objects.all()
    can_edit = request.user.is_authenticated and (
        request.user.is_superuser or 
        request.user.groups.filter(name='Editor').exists()
    )
    return render(request, 'home.html', {
        'sites': sites,
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
    model = apps.get_model(app_label='myapp', model_name=model_name)
    objects = model.objects.all()
    
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
            
    paginator = Paginator(objects, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.method == 'POST':
        object_data = {field: request.POST[field] for field in request.POST if field != 'csrfmiddlewaretoken'}
        try:
            obj = model.objects.create(**object_data)
            return JsonResponse({'success': True})
        except IntegrityError:
            return JsonResponse({'success': False, 'error': f"A {model_name} with this ID already exists."})
    
    headers = [{
        'name': field.name,
        'verbose_name': field.verbose_name,
        'is_primary_key': field.primary_key,
        'type': field.get_internal_type()
    } for field in model._meta.fields]
    
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
    })
    
@csrf_exempt
def delete_object(request, model_name, object_id):
    if request.method == 'POST':
        model = apps.get_model(app_label='myapp', model_name=model_name)
        # Dynamically get the primary key field name
        pk_field = model._meta.pk.name
        obj = get_object_or_404(model, **{pk_field: object_id})
        obj.delete()
        # Get the redirect URL from the query parameters
        redirect_url = request.GET.get('redirect_url', 'sites')
        return redirect(redirect_url)  # Redirect to the specified URL
    return HttpResponse(status=405)  # Method Not Allowed if not POST

import json
from django.views.decorators.http import require_POST

@require_POST
@csrf_exempt
def update_object(request, model_name, object_id):
    try:
        model = apps.get_model(app_label='myapp', model_name=model_name)
        obj = model.objects.get(pk=object_id)
        data = json.loads(request.body)
        for key, value in data.items():
            field_name = key.replace('field', '')
            setattr(obj, field_name, value)
        obj.save()
        return HttpResponse(json.dumps({'success': True}), content_type='application/json')
    except model.DoesNotExist:
        return HttpResponse(json.dumps({'success': False, 'error': f'{model_name} not found'}), content_type='application/json')
    except Exception as e:
        return HttpResponse(json.dumps({'success': False, 'error': str(e)}), content_type='application/json')