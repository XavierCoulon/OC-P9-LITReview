from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserFollows
from .forms import UserFollowsForm, SignUpForm


# View for index
def index(request):
	return render(request, "index.html")


# View for sign up
class SignUpView(CreateView):
	model = User
	template_name = "signup.html"
	form_class = SignUpForm
	success_url = reverse_lazy("index")


# View for follow up
class UserFollowsCreateView(LoginRequiredMixin, CreateView):
	model = UserFollows
	template_name = "create_followup.html"
	form_class = UserFollowsForm
	success_url = reverse_lazy("create_followup")

	def form_valid(self, form):
		# In case user already followed
		try:
			return super(UserFollowsCreateView, self).form_valid(form)
		except IntegrityError:
			raise ValidationError("Abonnement déjà existant!")

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs["user"] = self.request.user
		return kwargs

	def get_context_data(self, **kwargs):
		context = super(UserFollowsCreateView, self).get_context_data(**kwargs)
		followups = UserFollows.objects.filter(user=self.request.user)
		context["followups"] = followups
		followers = UserFollows.objects.filter(followed_user=self.request.user)
		context["followers"] = followers
		return context


@login_required
def delete_followup(request, id):
	followup = UserFollows.objects.get(pk=id)
	followup.delete()
	return redirect("create_followup")
