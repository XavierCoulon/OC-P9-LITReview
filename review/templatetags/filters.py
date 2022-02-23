from django import template

register = template.Library()


# Filtre pour affichage des étoiles "rating" au niveau d'une critique
@register.filter(name="rating")
def rating(note):
    return range(1, note+1)
