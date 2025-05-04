"""Админка для избранного."""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from .models import Favorite


@admin.register(Favorite)
class FavoriteAdmin(ModelAdmin):
    """Админка для избранного."""

    list_display = (
        "id",
        "user",
        "recipe",
    )
    list_display_links = ("user",)
    search_fields = ("user__username",)
    list_filter = ("user",)
    ordering = ("-created",)
    list_per_page = 20
    readonly_fields = ("created",)
    fieldsets = (
        (
            _("Общая информация"),
            {
                "fields": (
                    "user",
                    "recipe",
                    "created",
                )
            },
        ),
    )
