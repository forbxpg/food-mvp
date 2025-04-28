from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from unfold.admin import TabularInline, ModelAdmin

from .models import FavoriteRecipe, Favorite


class FavoriteRecipeInline(TabularInline):
    """Inline для избранных рецептов."""

    model = FavoriteRecipe
    extra = 0
    fk_name = "favorite"
    fields = ("recipe",)
    readonly_fields = ("recipe",)


@admin.register(Favorite)
class FavoriteAdmin(ModelAdmin):
    inlines = (FavoriteRecipeInline,)
    fields = ("user", "recipes_count")
    list_display = ("id", "user", "recipes_count")
    readonly_fields = ("user", "recipes_count")
    list_display_links = ("id", "user")
    search_fields = ("user__username", "id")

    def recipes_count(self, obj):
        """Количество рецептов в избранном."""
        return FavoriteRecipe.objects.filter(favorite=obj).count()

    recipes_count.short_description = _("Количество рецептов")
