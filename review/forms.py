from django.forms import ModelForm, forms, CharField
from review.models import Ticket, Review


class TicketCreateForm(ModelForm):
	class Meta:
		model = Ticket
		exclude = ["user"]
		labels = {
			"title": "Titre",
		}


class ReviewCreateForm(ModelForm):
	class Meta:
		model = Review
		fields = ["rating", "headline", "body"]
		labels = {
			"headline": "Titre",
			"body": "Description"
		}


class TicketForm(ModelForm):
	class Meta:
		model = Ticket
		exclude = ["user"]
		labels = {
			"title": "Titre",
		}


class ReviewForm(ModelForm):
	class Meta:
		model = Review
		exclude = ["user", "ticket"]
		labels = {
			"headline": "Titre",
			"body": "Description",
		}


class SearchForm(forms.Form):
	titre = CharField(max_length=30, required=True)
	auteur = CharField(max_length=30, required=True)


