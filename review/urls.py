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
from .views import index, TicketCreateView, TicketUpdateView, TicketDetailView, ReviewCreateView, create_ticket_review, flux


urlpatterns = [
    path("", index, name="index"),
    path("flux/", flux, name="flux"),
    path("create_ticket/", login_required(TicketCreateView.as_view()), name="create_ticket"),
    path("create_review/", login_required(ReviewCreateView.as_view()), name="create_review"),
    path("create_ticket_review/", login_required(create_ticket_review), name="create_review"),
    path("update_ticket/<str:pk>/", login_required(TicketUpdateView.as_view()), name="update_ticket"),
    path("view_ticket/<str:pk>/", login_required(TicketDetailView.as_view()), name="view_ticket"),
    ]