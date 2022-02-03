from django.contrib import admin
from mvp.models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
	list_display = (
		"title",
		"description",
		"user",
		"image",
	)
