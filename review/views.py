import requests
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Value, CharField, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from review.models import Ticket, Review
from review.forms import TicketForm, ReviewForm
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
	# Liste des critiques de l'utilisateur + celles des utilisateurs suivis + celles dont le ticket a été créé par l'utilisateur
	reviews = Review.objects.filter(
		Q(user_id=user) | Q(user_id__in=followed_users) | Q(ticket__in=tickets)
	)
	return reviews


@login_required
def flux(request):

	tickets = viewable_tickets(request.user)[0]
	tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
	reviews = viewable_reviews(request.user)
	reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))

	posts = sorted(
		chain(tickets, reviews),
		key=lambda post: post.time_created,
		reverse=True
	)

	tickets_with_review = viewable_tickets(request.user)[1]

	return render(request, "flux.html", context={"posts": posts, "tickets_with_review": tickets_with_review })


@login_required
def myposts(request):
	tickets = Ticket.objects.filter(user=request.user)
	tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
	reviews = Review.objects.filter(user=request.user)
	reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))

	posts = sorted(
		chain(tickets, reviews),
		key=lambda post: post.time_created,
		reverse=True
	)

	return render(request, "myposts.html", context={"posts": posts})


def search(request):
	response = requests.get("https://www.googleapis.com/books/v1/volumes?q=intitle:au bonheur des dames+inauthor:zola")
	data = response.json()
	books = data["items"]
	return render(request, "search.html", {"books": books})


class SignUpView(CreateView):
	model = User
	template_name = "signup.html"
	form_class = UserCreationForm
	success_url = reverse_lazy("login")


class TicketCreateView(LoginRequiredMixin, CreateView):
	model = Ticket
	template_name = "create_ticket.html"
	fields = ["title", "description", "image"]
	success_url = reverse_lazy("flux")

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(TicketCreateView, self).form_valid(form)


class TicketDetailView(LoginRequiredMixin, DetailView):
	model = Ticket
	template_name = "view_ticket.html"
	context_object_name = "ticket"


class SnippetTicketDetailView(LoginRequiredMixin, DetailView):
	model = Ticket
	template_name = "view_snippet_ticket.html"
	context_object_name = "ticket"


class TicketUpdateView(LoginRequiredMixin, UpdateView):
	model = Ticket
	template_name = "update_ticket.html"
	fields = ["title", "description", "image"]
	success_url = reverse_lazy("myposts")

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(TicketUpdateView, self).form_valid(form)


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
	model = Review
	template_name = "update_review.html"
	fields = ["rating", "headline", "body"]
	success_url = reverse_lazy("myposts")

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(ReviewUpdateView, self).form_valid(form)


class ReviewCreateView(LoginRequiredMixin, CreateView):
	model = Review
	template_name = "create_review.html"
	fields = ["rating", "headline", "body"]
	success_url = reverse_lazy("flux")

	def get_context_data(self, **kwargs):
		context = super(ReviewCreateView, self).get_context_data(**kwargs)
		ticket_id = self.request.GET.get("ticket_id")
		ticket = Ticket.objects.get(pk=ticket_id)
		context["ticket"] = ticket
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		ticket_id = self.request.GET.get("ticket_id")
		form.instance.ticket = Ticket.objects.get(pk=ticket_id)
		return super(ReviewCreateView, self).form_valid(form)


class ReviewDetailView(LoginRequiredMixin, DetailView):
	model = Review
	template_name = "view_review.html"
	context_object_name = "review"
	# success_url = reverse_lazy("flux")

	def get_context_data(self, **kwargs):
		context = super(ReviewDetailView, self).get_context_data(**kwargs)
		ticket = Review.objects.get(pk=self.kwargs["pk"])
		print(ticket.ticket_id)
		ticket = Ticket.objects.get(pk=ticket.ticket_id)
		print(ticket.__dict__)
		context["ticket"] = ticket
		return context


@login_required
def delete_ticket(request, pk):
	ticket = Ticket.objects.get(pk=pk)
	ticket.delete()
	return redirect("myposts")


@login_required
def delete_review(request, pk):
	review = Review.objects.get(pk=pk)
	review.delete()
	return redirect("myposts")


@login_required
def create_ticket_review(request):
	ticket_form = TicketForm()
	review_form = ReviewForm()

	if request.method == "POST":
		ticket_form = TicketForm(request.POST, request.FILES)
		review_form = ReviewForm(request.POST)
		if ticket_form.is_valid() and review_form.is_valid():
			ticket = ticket_form.save(commit=False)
			ticket.user = request.user
			ticket.save()
			review = review_form.save(commit=False)
			review.user = request.user
			review.ticket = ticket
			review.save()
		return HttpResponseRedirect("../flux")
	return render(request, "create_ticket_review.html", context={"ticket": ticket_form, "review": review_form})



