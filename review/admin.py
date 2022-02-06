from django.contrib import admin

from review.models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
	list_display = (
		"title",
		"description",
		"user",
		"image",
	)
