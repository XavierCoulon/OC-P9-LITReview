import requests
from urllib.request import urlopen
from django.db.models import Q
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Ticket, Review
from users.models import UserFollows


def viewable_tickets(user):
	"""
	Select tickets to display in "flux" (cf. doc for detailes rules)

	Args:
		user: user logged

	Returns:
		tickets, and among these tickets the ones with review (tuple of Queryset)
	"""
	# Followed users' list
	followed_users = [user.followed_user for user in UserFollows.objects.filter(user_id=user)]
	# List of tickets with review
	tickets_with_review_ids = [review.ticket_id for review in Review.objects.all()]
	# User's tickets + followed users' list
	tickets = Ticket.objects.filter(
		Q(user_id=user) | Q(user_id__in=followed_users)
	)
	# Tickets with review on filtered tickets
	tickets_with_review = tickets.filter(id__in=tickets_with_review_ids)

	return tickets, tickets_with_review


def viewable_reviews(user):
	"""
		Select reviews to display in "flux" (cf. doc for detailes rules)

		Args:
			user: user logged

		Returns:
			reviews (Queryset)
		"""
	# Followed users' list
	followed_users = [user.followed_user for user in UserFollows.objects.filter(user_id=user)]
	# User's tickets
	tickets = [ticket.id for ticket in Ticket.objects.filter(user_id=user)]
	# User's reviews + followed users' ones + the ones whose have benne created by user
	reviews = Review.objects.filter(
		Q(user_id=user) | Q(user_id__in=followed_users) | Q(ticket__in=tickets)
	)
	return reviews


def get_books_with_pic(request, form):
	"""
	Use Googe Books API to find books with pictures
	Args:
		request: request
		form: result of search form (title + author from template 'search'

	Returns:
		Results of the search in search template

	"""
	response = requests.get(
		f"https://www.googleapis.com/books/v1/volumes?q=intitle:{form.cleaned_data['titre']}"
		f"+inauthor:{form.cleaned_data['auteur']}")
	data = response.json()

	# If no result in API
	if data["totalItems"] == 0:
		messages.warning(request, "Pas de résultat.")
		return render(request, "search.html", {"search_form": form})
	else:
		books = data["items"]
		# Look for results including a pic, max 10 results
		books_with_pic = []
		for i in range(0, min(len(books), 10)):
			if "imageLinks" in books[i]["volumeInfo"]:
				books_with_pic.append(books[i])
		if len(books_with_pic) == 0:
			messages.warning(request, "Pas de résultat intégrant une image.")
		return render(request, "search.html", {"search_form": form, "books": books_with_pic})


def get_book_data(request, google_id):
	"""
	Ceeate a ticket from Google Books API result
	Args:
		request: request
		google_id: google book ID

	Returns:
		Create a Ticket model, and redirect to myposts view
	"""
	response = requests.get(f"https://www.googleapis.com/books/v1/volumes/{google_id}")
	data = response.json()
	book = data["volumeInfo"]
	img_temp = NamedTemporaryFile(delete=True)
	img_temp.write(urlopen(book['imageLinks']['smallThumbnail']).read())
	img_temp.flush()

	ticket = Ticket(
		title=f"{book['title']} - {book['authors'][0]}",
		description="Demande effectuée via la recherche Google Books",
		user=request.user
	)

	ticket.image.save(f"{google_id}.jpg", File(img_temp))
	ticket.save()

	return redirect("myposts")
