from django.shortcuts import render
from django.http import HttpResponse
from .models import Site

def home(request):
    # return HttpResponse("Hello, Django!")
    
    sites = Site.objects.all()
    
    # Pass the sites data to the 'home.html' template
    return render(request, 'home.html', {'sites': sites})
    

