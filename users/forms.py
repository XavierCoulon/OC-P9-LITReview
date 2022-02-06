from django.contrib.auth.models import User
from django.forms import ModelForm, forms, ChoiceField, ModelChoiceField
from django.http import request
from users.models import UserFollows


class UserFollowsForm(ModelForm):
	class Meta:
		model = UserFollows
		fields = "__all__"

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop("request")
		super(UserFollowsForm, self).__init__(*args, **kwargs)
		self.fields["followed_user"] = ModelChoiceField(queryset=User.objects.exclude(pk=self.request.user.pk))
