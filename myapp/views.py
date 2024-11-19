from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.utils import IntegrityError
from .models import Site

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
    

