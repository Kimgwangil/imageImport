from django import template

register = template.Library()

@register.filter(name='time')
def times(number):
    return range(number)