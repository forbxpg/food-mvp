from django.contrib import admin
from django.contrib.auth.models import AbstractUser

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "avatar",
        "is_subscribed",
        "is_staff",
        "is_active",
        "is_superuser",
        "last_login",
        "date_joined",
    )
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
    )
