from itertools import chain
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Value, CharField
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from review.models import Ticket, Review
from review.forms import TicketForm, ReviewForm, TicketCreateForm, ReviewCreateForm, SearchForm
from review.controller import viewable_tickets, viewable_reviews, get_books_with_pic


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


@login_required()
def search(request):
	if request.method == 'POST':
		search_form = SearchForm(request.POST)
		if search_form.is_valid():
			return get_books_with_pic(request, search_form)
	else:
		search_form = SearchForm()
		return render(request, "search.html", {"search_form": search_form})


class SignUpView(CreateView):
	model = User
	template_name = "signup.html"
	form_class = UserCreationForm
	success_url = reverse_lazy("login")


class TicketCreateView(LoginRequiredMixin, CreateView):
	model = Ticket
	template_name = "create_ticket.html"
	form_class = TicketCreateForm
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
	form_class = ReviewCreateForm
	success_url = reverse_lazy("flux")

	def get_context_data(self, **kwargs):
		context = super(ReviewCreateView, self).get_context_data(**kwargs)
		ticket_id = self.kwargs["pk"]
		ticket = Ticket.objects.get(pk=ticket_id)
		context["ticket"] = ticket
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		ticket_id = self.kwargs["pk"]
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



