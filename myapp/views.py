from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.utils import IntegrityError
from .models import Site

from django.shortcuts import redirect, get_object_or_404
from django.apps import apps

def home(request):
    sites = Site.objects.all()
    return render(request, 'home.html', {'sites': sites})

def sites(request):
    if request.method == 'POST':
        site_data = {field: request.POST[field] for field in request.POST if field != 'csrfmiddlewaretoken'}
        try:
            Site.objects.create(**site_data)
        except IntegrityError:
            return render(request, 'sites.html', {
                'sites': Site.objects.all(),
                'headers': [field.name for field in Site._meta.fields],
                'error': 'A site with this Site_num already exists.'
            })
        return redirect('sites')
    
    sites = Site.objects.all()
    
    headers = [{'name': field.name, 'verbose_name': field.verbose_name} for field in Site._meta.fields]
    
    # if sites.exists():
    #     headers = sites.first()._meta.fields
    # else:
    #     headers = []
    
    return render(request, 'sites.html', {'sites': sites, 'headers': headers})

def delete_object(request, model_name, object_id):
    model = apps.get_model(app_label='myapp', model_name=model_name)
    obj = get_object_or_404(model, SiteID=object_id)
    obj.delete()
    return redirect('sites') 
    

