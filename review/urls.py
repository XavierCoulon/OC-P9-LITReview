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
from django.urls import path
from .controller import get_book_data
from .views import TicketCreateView, TicketUpdateView, ReviewCreateView, create_ticket_review, flux, ReviewUpdateView,\
    myposts, delete_review, delete_ticket, search

urlpatterns = [
    path("flux/", flux, name="flux"),
    path("myposts/", myposts, name="myposts"),
    path("search/", search, name="search"),
    path("search/<str:google_id>", get_book_data, name="google"),
    path("ticket/", TicketCreateView.as_view(), name="create_ticket"),
    path("ticket/<int:pk>/update", TicketUpdateView.as_view(), name="update_ticket"),
    path("ticket/<int:pk>/delete", delete_ticket, name="delete_ticket"),
    path("ticket/<int:pk>/review", ReviewCreateView.as_view(), name="create_review"),
    path("review/<int:pk>/update/", ReviewUpdateView.as_view(), name="update_review"),
    path("review/<int:pk>/delete", delete_review, name="delete_review"),
    path("ticket_review/", create_ticket_review, name="create_ticket_review"),
]
