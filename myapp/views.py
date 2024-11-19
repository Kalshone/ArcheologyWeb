from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.utils import IntegrityError
from .models import Site

from django.shortcuts import redirect, get_object_or_404
from django.apps import apps
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlencode
from django.contrib import messages

def home(request):
    sites = Site.objects.all()
    return render(request, 'home.html', {'sites': sites})

def sites(request):
    if request.method == 'POST':
        site_data = {field: request.POST[field] for field in request.POST if field != 'csrfmiddlewaretoken'}
        try:
            Site.objects.create(**site_data)
        except IntegrityError:
            messages.error(request, "A site with this number already exists.")
            return redirect('sites')
    
    sites = Site.objects.all()
    headers = [{'name': field.name, 'verbose_name': field.verbose_name} for field in Site._meta.fields]
    return render(request, 'sites.html', {'sites': sites, 'headers': headers})

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

