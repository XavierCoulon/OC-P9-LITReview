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
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from .views import SignUpView, flux, index, TicketCreateView, TicketUpdateView, UserFollowsCreateView, ReviewCreateView, create_ticket_review

urlpatterns = [
    path("", index, name="index"),
    path("admin/", admin.site.urls),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/profile/", flux, name="flux"),
    path("create_ticket/", login_required(TicketCreateView.as_view()), name="create_ticket"),
    path("create_review/", login_required(ReviewCreateView.as_view()), name="create_review"),
    path("create_ticket_review/", login_required(create_ticket_review), name="create_review"),
    path("update_ticket/<str:pk>/", login_required(TicketUpdateView.as_view()), name="update_ticket"),
    path("create_followup/", login_required(UserFollowsCreateView.as_view()), name="create_followup"),
]
