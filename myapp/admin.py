from django.contrib import admin
from .models import EditorTablePermission, EditorRegistrationCode
from django import forms
from django.apps import apps

class EditorTablePermissionForm(forms.ModelForm):
    # Create choices from all available model names in myapp
    model_choices = [(model.__name__, model.__name__) for model in apps.get_app_config('myapp').get_models()]
    table_name = forms.ChoiceField(choices=model_choices)
    
    class Meta:
        model = EditorTablePermission
        fields = '__all__'

@admin.register(EditorTablePermission)
class EditorTablePermissionAdmin(admin.ModelAdmin):
    form = EditorTablePermissionForm
    list_display = ('editor', 'table_name', 'can_add', 'can_edit', 'can_delete')
    list_filter = ('table_name', 'can_add', 'can_edit', 'can_delete')
    search_fields = ('editor__username', 'table_name')

@admin.register(EditorRegistrationCode)
class EditorRegistrationCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_used')
    search_fields = ('code',)
    list_filter = ('is_used',)