# Django
from django.contrib import admin
from django.contrib.sessions.models import Session


class SessionsAdmin(admin.ModelAdmin):
    list_display = ["session_key", "expire_date"]
    ordering = ["session_key"]


admin.site.register(Session, SessionsAdmin)
