from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from users.models import UserFollows
from users.forms import UserFollowsForm


def index(request):
	return render(request, "index.html")


class SignUpView(CreateView):
	model = User
	template_name = "signup.html"
	form_class = UserCreationForm
	success_url = reverse_lazy("login")


# def subscription(request):
# 	form = SubscriptionForm()
# 	if request.method == "POST":
# 		followed = SubscriptionForm(request.POST).data["search"]
# 		if User.objects.get(username=followed):
# 			print("OK")
# 			print(User.objects.get(username=followed).id)
# 			UserFollows.objects.create(followed_user=User.objects.get(username=followed), user=request.user)
#
# 	return render(request, "subscription.html", {"form": form})


class UserFollowsCreateView(CreateView):
	model = UserFollows
	template_name = "create_followup.html"
	form_class = UserFollowsForm
	success_url = reverse_lazy("flux")

	# def get_form_kwargs(self):
	# 	kwargs = super(UserFollowsForm, self).get_form_kwargs()
	# 	kwargs["request"] = self.request
	# 	return kwargs

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super(UserFollowsCreateView, self).form_valid(form)

