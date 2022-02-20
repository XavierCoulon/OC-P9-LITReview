from django.forms import ModelForm
from review.models import Ticket, Review


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

