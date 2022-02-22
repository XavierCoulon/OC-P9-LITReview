import requests
from urllib.request import urlopen
from django.db.models import Q
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from django.shortcuts import redirect, render
from django.contrib import messages
from review.models import Ticket, Review
from users.models import UserFollows


def viewable_tickets(user):

	# Liste des utilisateur suivis
	followed_users = [user.followed_user for user in UserFollows.objects.filter(user_id=user)]
	# Liste des tickets ayant une critique
	tickets_with_review_ids = [review.ticket_id for review in Review.objects.all()]
	# Liste des tickets: ceux de l'utilisateur + ceux dont les utilisateurs sont dans l'abonnement
	tickets = Ticket.objects.filter(
		Q(user_id=user) | Q(user_id__in=followed_users)
	)
	# Liste des tickets avec critique
	tickets_with_review = tickets.filter(id__in=tickets_with_review_ids)

	return tickets, tickets_with_review


def viewable_reviews(user):

	# Liste des utilisateur suivis
	followed_users = [user.followed_user for user in UserFollows.objects.filter(user_id=user)]
	# Liste des tickets de l'utilisateur
	tickets = [ticket.id for ticket in Ticket.objects.filter(user_id=user)]
	# Liste des critiques de l'utilisateur + utilisateurs suivis + dont le ticket a été créé par l'utilisateur
	reviews = Review.objects.filter(
		Q(user_id=user) | Q(user_id__in=followed_users) | Q(ticket__in=tickets)
	)
	return reviews


def get_books_with_pic(request, form):

	response = requests.get(
		f"https://www.googleapis.com/books/v1/volumes?q=intitle:{form.cleaned_data['titre']}"
		f"+inauthor:{form.cleaned_data['auteur']}")
	data = response.json()
	if data["totalItems"] == 0:
		messages.warning(request, "Pas de résultat.")
		return render(request, "search.html", {"search_form": form})
	else:
		books = data["items"]
		books_with_pic = []
		for i in range(0, min(len(books), 10)):
			if "imageLinks" in books[i]["volumeInfo"]:
				books_with_pic.append(books[i])
		if len(books_with_pic) == 0:
			messages.warning(request, "Pas de résultat intégrant une image.")
		return render(request, "search.html", {"search_form": form, "books": books_with_pic})


def get_book_data(request, google_id):

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
