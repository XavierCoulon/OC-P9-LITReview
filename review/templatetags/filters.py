from django import template

register = template.Library()


@register.filter(name="rating")
def rating(note):
    return range(1, note+1)
