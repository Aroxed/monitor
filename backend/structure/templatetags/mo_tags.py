from django import template

from structure.models import MonitoringObject

register = template.Library()


@register.simple_tag
def get_mo_list():
    return list(MonitoringObject.objects.all())


@register.filter()
def to_int(value):
    return int(value)
