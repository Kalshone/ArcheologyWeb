from django import template

register = template.Library()

@register.filter
def attr(obj, attr_name):
    return getattr(obj, attr_name)

# @register.filter
# def get_site_data(site):
#     return {field.name: getattr(site, field.name) for field in site._meta.fields}