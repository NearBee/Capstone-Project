from django import template

register = template.Library()


@register.filter
def dictkey(value, arg):
    return value.get(arg)
