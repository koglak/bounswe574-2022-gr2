from django import template

register = template.Library()

from ..models import Course

@register.simple_tag
def total_courses():
    return Course.published.count()