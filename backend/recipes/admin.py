"""Админка приложения recipes."""

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin, TabularInline

from .models import Ingredient, Recipe, RecipeIngredient, Tag


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    """Админка для тегов."""

    list_display = ("id", "name", "slug")
    search_fields = ("name", "slug")
    list_display_links = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Ingredient)
class IngredientAdmin(ModelAdmin):
    """Админка для ингридиентов."""

    list_display = ("id", "name", "measurement_unit")
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"
    list_editable = ("measurement_unit",)
    list_display_links = ("id", "name")


class RecipeIngredientInline(TabularInline):
    model = RecipeIngredient
    extra = 0
    fk_name = "recipe"
    fields = (
        "ingredient",
        "amount",
    )
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_display = (
        "id",
        "name",
        "author_link",
        "cooking_time",
        "created_at",
        "favorites_count",
    )
    fields = (
        "name",
        "author",
        "tags",
        "text",
        "cooking_time",
        "image",
        "favorites_count",
        "link",
    )
    list_display_links = ("name",)
    readonly_fields = ("favorites_count",)

    def favorites_count(self, obj):
        return obj.favorites.count()

    favorites_count.short_description = _("Добавлений в избранное")

    def author_link(self, obj):
        author_url = reverse(
            "admin:users_user_change",
            args=(obj.author.id,),
        )
        return format_html(
            '<a href="{}">{}</a>',
            author_url,
            obj.author,
        )

    author_link.short_description = _("Автор")
    author_link.admin_order_field = "author"
