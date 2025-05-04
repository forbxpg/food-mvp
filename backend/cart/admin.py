"""Админка для корзины."""

from cart.models import Cart
from django.contrib import admin
from unfold.admin import ModelAdmin


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    """Админка для корзины."""

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
            "Общая информация",
            {
                "fields": (
                    "user",
                    "recipe",
                    "created",
                )
            },
        ),
    )
