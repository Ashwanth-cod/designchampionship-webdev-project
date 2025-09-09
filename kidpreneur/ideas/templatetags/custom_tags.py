from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    try:
        return dictionary.get(key)
    except AttributeError:
        return None

from django import template

register = template.Library()

@register.filter
def dict_get(dict_data, key):
    """Get a value from a dictionary by key."""
    return dict_data.get(key)
