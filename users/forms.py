from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import ModelForm, CharField
from users.models import UserFollows


class UserLoginForm(AuthenticationForm):

	def __init__(self, *args, **kwargs):
		super(UserLoginForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['placeholder'] = "Nom d'utilisateur"
		self.fields['password'].widget.attrs['placeholder'] = "Mot de passe"


class SignUpForm(UserCreationForm):

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['placeholder'] = "Nom d'utilisateur"
		self.fields['password1'].widget.attrs['placeholder'] = "Mot de passe"
		self.fields['password2'].widget.attrs['placeholder'] = "Confirmation Mot de passe"
		self.fields["password1"].help_text = None
		self.fields["password2"].help_text = None
		self.fields["username"].help_text = None


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






