from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.forms import ModelForm, Form, CharField, TextInput
from users.models import UserFollows


#User = get_user_model()


class UserFollowsForm(ModelForm):
	followed_user = CharField(required=True)

	class Meta:
		model = UserFollows
		fields = ["followed_user"]

	def __init__(self, user, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.user = user

	def clean_followed_user(self):
		username = self.cleaned_data["followed_user"]
		try:
			followed_user = User.objects.get(username=username)
		except User.DoesNotExist:
			raise ValidationError("Followed user does not exist")
		if self.user.username == username:
			raise ValidationError("Vous ne pouvez pas vous abonner à vous-même ;-)")

		try:
			UserFollows.objects.get(followed_user=followed_user, user=self.user)
			raise ValidationError("Abonnement déjà existant!")
		except UserFollows.DoesNotExist:
			pass

		return followed_user

	def save(self, commit="True"):
		instance = super().save(commit=False)
		instance.user = self.user
		if commit:
			instance.save()
		return instance






