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
from django.urls import path
from .views import TicketCreateView, TicketUpdateView, TicketDetailView, ReviewCreateView, create_ticket_review, flux, \
    ReviewDetailView, ReviewUpdateView, myposts, delete_review, delete_ticket, SnippetTicketDetailView

urlpatterns = [
    path("flux/", flux, name="flux"),
    path("myposts/", myposts, name="myposts"),
    path("create_ticket/", login_required(TicketCreateView.as_view()), name="create_ticket"),
    path("create_review/", login_required(ReviewCreateView.as_view()), name="create_review"),
    path("create_ticket_review/", login_required(create_ticket_review), name="create_ticket_review"),
    path("update_ticket/<int:pk>/", login_required(TicketUpdateView.as_view()), name="update_ticket"),
    path("update_review/<int:pk>/", login_required(ReviewUpdateView.as_view()), name="update_review"),
    path("view_ticket/<int:pk>/", login_required(TicketDetailView.as_view()), name="view_ticket"),
    path("view_snippet_ticket/<int:pk>/", login_required(SnippetTicketDetailView.as_view()), name="view_snippet_ticket"),
    path("view_review/<int:pk>/", login_required(ReviewDetailView.as_view()), name="view_review"),
    path("delete_ticket/<int:pk>/", delete_ticket, name="delete_ticket"),
    path("delete_review/<int:pk>/", delete_review, name="delete_review"),
    ]