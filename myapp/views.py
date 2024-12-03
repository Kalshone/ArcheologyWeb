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
import json

def landing_page(request):
    # Render the landing page template
    return render(request, 'landing.html')

def login(request):
    # Redirect to the dashboard view
    return redirect('dashboard')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def dashboard(request):
    sites = Site.objects.all()
    return render(request, 'home.html', {'sites': sites})

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
    
    if request.method == 'POST':
        object_data = {field: request.POST[field] for field in request.POST if field != 'csrfmiddlewaretoken'}
        try:
            obj = model.objects.create(**object_data)
            return JsonResponse({'success': True})
        except IntegrityError:
            return JsonResponse({'success': False, 'error': f"A {model_name} with this ID already exists."})
    
    objects = model.objects.all()
    headers = [{
        'name': field.name,
        'verbose_name': field.verbose_name,
        'is_primary_key': field.primary_key,
        'type': field.get_internal_type()
    } for field in model._meta.fields]
    
    return render(request, 'table_view.html', {
        'objects': objects,
        'headers': headers,
        'model_name': model_name
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