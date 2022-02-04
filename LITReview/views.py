from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from mvp.models import Ticket, UserFollows, Review
from mvp.forms import TicketForm, ReviewForm


def index(request):
	return render(request, "index.html")


@login_required
def flux(request):
	tickets = Ticket.objects.filter(user_id=request.user)
	reviews = Review.objects.filter(user_id=request.user)
	return render(request, "flux.html", context={"tickets": tickets, "reviews": reviews})


class SignUpView(CreateView):
	model = User
	template_name = "signup.html"
	form_class = UserCreationForm
	success_url = reverse_lazy("login")


class TicketCreateView(CreateView):
	model = Ticket
	template_name = "create_ticket.html"
	fields = ["title", "description", "image"]
	success_url = reverse_lazy("flux")

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(TicketCreateView, self).form_valid(form)


class TicketUpdateView(UpdateView):
	model = Ticket
	template_name = "update_ticket.html"
	fields = ["title", "description", "image"]
	success_url = reverse_lazy("flux")

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(TicketUpdateView, self).form_valid(form)


class ReviewCreateView(CreateView):
	model = Review
	template_name = "create_review.html"
	fields = "__all__"
	success_url = reverse_lazy("flux")

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(ReviewCreateView, self).form_valid(form)


class UserFollowsCreateView(CreateView):
	model = UserFollows
	template_name = "create_followup.html"
	# personnalisation des valeurs du field où? Création obligatoire d'un customed form ?
	fields = ["followed_user"]
	success_url = reverse_lazy("flux")

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(UserFollowsCreateView, self).form_valid(form)


def create_ticket_review(request):
	if request.method == "POST":
		ticket_form = TicketForm(request.POST)
		review_form = ReviewForm(request.POST)
		if ticket_form.is_valid() and review_form.is_valid():
			ticket = ticket_form.save(commit=False)
			ticket.user = request.user
			ticket.save()
			review = review_form.save(commit=False)
			review.user = request.user
			review.ticket = ticket
			review.save()
		return HttpResponseRedirect(request.path)
	else:
		ticket_form = TicketForm()
		review_form = ReviewForm()

	return render(request, "create_ticket_review.html", context={"ticket": ticket_form, "review": review_form})



