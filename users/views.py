from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from users.models import UserFollows
from users.forms import UserFollowsForm


def index(request):
	return render(request, "index.html")


class SignUpView(CreateView):
	model = User
	template_name = "signup.html"
	form_class = UserCreationForm
	success_url = reverse_lazy("login")


class UserFollowsCreateView(CreateView):
	model = UserFollows
	template_name = "create_followup.html"
	form_class = UserFollowsForm
	success_url = reverse_lazy("create_followup")

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


def delete_followup(request, id):
	followup = UserFollows.objects.get(pk=id)
	followup.delete()
	return redirect("create_followup")


# class FollowUpDetailView(ListView):
# 	model = UserFollows
# 	template_name = "view_followup.html"
# 	context_object_name = "followed"
#
# 	def get_context_data(self, **kwargs):
# 		context = super(FollowUpDetailView, self).get_context_data(**kwargs)
# 		followups = UserFollows.objects.filter(user=self.request.user)
# 		context["followups"] = followups
# 		followers = UserFollows.objects.filter(followed_user=self.request.user)
# 		context["followers"] = followers
# 		return context
