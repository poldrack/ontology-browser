from django import template
import json
import ast

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

@register.filter
def format_description(value):
    """Format description by converting tuple/list of strings into a single string"""
    if not value:
        return ""
    
    # If it's already a string, return it
    if isinstance(value, str):
        return value
    
    # If it's a string representation of a tuple/list
    if isinstance(value, str) and (value.startswith('(') or value.startswith('[')):
        try:
            # Try to safely evaluate the string as a literal
            value = ast.literal_eval(value)
        except:
            return value

    # If it's a tuple or list, join the elements
    if isinstance(value, (tuple, list)):
        return ' '.join(value)
    
    return str(value) 