from django.shortcuts import render
from django.http import HttpResponse
from .models import Site

def home(request):
    return HttpResponse("Hello, Django!")
