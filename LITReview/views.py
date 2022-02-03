from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from mvp.models import Ticket, UserFollows, Review


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


class UserFollowsCreateView(CreateView):
	model = UserFollows
	template_name = "create_followup.html"
	# personnalisation des valeurs du field où? Création obligatoire d'un customed form ?
	fields = ["followed_user"]
	success_url = reverse_lazy("flux")

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(UserFollowsCreateView, self).form_valid(form)
