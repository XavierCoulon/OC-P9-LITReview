from django.forms import ModelForm, forms, CharField
from .models import Ticket, Review


# Form used for ticket creation
class TicketCreateForm(ModelForm):
	class Meta:
		model = Ticket
		exclude = ["user"]
		labels = {
			"title": "Titre",
		}


# Form used for review creation
class ReviewCreateForm(ModelForm):
	class Meta:
		model = Review
		fields = ["rating", "headline", "body"]
		labels = {
			"headline": "Titre",
			"body": "Description"
		}


# Form used for Google Books API
class SearchForm(forms.Form):
	titre = CharField(max_length=30, required=True)
	auteur = CharField(max_length=30, required=True)
