from django import template

register = template.Library()

@register.filter
def filter_permission(permissions, args):
    editor, table = args
    try:
        return permissions.get(editor=editor, table_name=table)
    except:
        return None