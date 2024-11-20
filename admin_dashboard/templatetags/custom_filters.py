from django import template
from django.db.models import Model

register = template.Library()

@register.filter(name='attr')
def attr(obj, field_name):
    """
    Get the value of a field dynamically from a model instance.
    """
    if isinstance(obj, Model):
        return getattr(obj, field_name, None)
    return None
