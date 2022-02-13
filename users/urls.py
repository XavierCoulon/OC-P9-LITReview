"""LITReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import path, include

from .forms import UserLoginForm
from .views import SignUpView, UserFollowsCreateView, delete_followup

urlpatterns = [
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
    path("", LoginView.as_view(template_name="registration/login.html", authentication_form=UserLoginForm), name="login"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("create_followup/", login_required(UserFollowsCreateView.as_view()), name="create_followup"),
    path("delete_followup/<int:id>/", delete_followup, name="delete_followup"),
]
