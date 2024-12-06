from django import template

register = template.Library()

@register.filter
def attr(obj, attr_name):
    return getattr(obj, attr_name)

@register.filter
def filter_permission(permissions, args):
    try:
        editor_id, table_name = args.split(',')
        return permissions.get(editor_id=editor_id, table_name=table_name)
    except (ValueError, AttributeError):
        return None