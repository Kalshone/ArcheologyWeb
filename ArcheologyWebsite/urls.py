"""
URL configuration for ArcheologyWebsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page, name='landing_page'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login, name='login'),
    path("signup/", views.signup, name="signup"),
    # path('', include('myapp.urls')),
    
    path('sites/', views.sites, name='sites'),
    # path('areas/', views.areas, name='areas'),
    # path('pottery/', views.pottery, name='pottery'),
    # path('artifacts/', views.artifacts, name='artifacts'),
    
    path('delete/<str:model_name>/<int:object_id>/', views.delete_object, name='delete_object'),
    path('update_object/<str:model_name>/<int:object_id>/', views.update_object, name='update_object'), 
    
    path("accounts/", include("django.contrib.auth.urls")),
    # path("accounts/", include("accounts.urls")),
]
