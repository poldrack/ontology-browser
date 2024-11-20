from django import template
import json

register = template.Library()

@register.filter
def format_id(value):
    """Format IDs by removing prefixes and replacing underscores with spaces"""
    if value and isinstance(value, str):
        if value.startswith('construct-'):
            value = value[10:]  # Remove 'construct-' prefix
        return value.replace('_', ' ')
    return value

@register.filter
def format_list(value):
    """Format any list-like value as a proper list"""
    if not value:
        return []
    
    # If the value is a string (JSON), parse it
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            return [value]
    
    # If it's already a list, return it
    if isinstance(value, list):
        return value
    
    # If it's neither, wrap it in a list
    return [value] 