from django import template

register = template.Library()

@register.filter
def format_id(value):
    """Format IDs by removing prefixes and replacing underscores with spaces"""
    if value and isinstance(value, str):
        if value.startswith('construct-'):
            value = value[10:]  # Remove 'construct-' prefix
        return value.replace('_', ' ')
    return value 