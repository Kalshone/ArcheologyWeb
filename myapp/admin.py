from django.contrib import admin
from .models import EditorTablePermission

@admin.register(EditorTablePermission)
class EditorTablePermissionAdmin(admin.ModelAdmin):
    list_display = ('editor', 'table_name', 'can_add', 'can_edit', 'can_delete')
    list_filter = ('table_name', 'can_add', 'can_edit', 'can_delete')
    search_fields = ('editor__username', 'table_name')