from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.forms import ModelForm, Form, CharField, TextInput
from django.shortcuts import get_object_or_404
from users.models import UserFollows


class UserFollowsForm(ModelForm):

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop("user", None)
		super(UserFollowsForm, self).__init__(*args, **kwargs)

	class Meta:
		model = UserFollows
		fields = ["followed_user"]
		#widgets = {"followed_user": TextInput}

	# def clean_followed_user(self):
	# 	# Test code de Benjamin
	# 	print("clean")
	# 	username = self.cleaned_data.get("followed_user", None)
	# 	print(username)
	# 	users = User.objects.all()
	# 	if username == str(self.user):
	# 		raise ValidationError("Vous ne pouvez pas vous follow")
	# 	elif username not in [user.username for user in users]:
	# 		raise ValidationError("Cet utilisateur n'existe pas")
	# 	else:
	# 		followed_user = get_object_or_404(User, username=username)
	# 	return followed_user

	# def save(self, commit=True):
	# 	# user_follow = super(FollowForm, self).save(commit=False)
	# 	print("save")
	# 	if commit:
	# 		try:
	# 			self.instance.save()
	# 		# user_follow.save()
	# 		except IntegrityError:
	# 			raise ValidationError("Cet utilisateur est déjà follow")
	# 	# return user_follow
	# 	return self.instance







