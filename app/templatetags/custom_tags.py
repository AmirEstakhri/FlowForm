# app/templatetags/custom_tags.py
from django import template

register = template.Library()

@register.filter
def has_subrole(user, subrole_name):
    return user.has_subrole(subrole_name)
