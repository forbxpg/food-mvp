from django.contrib import admin

from favorite.models import Favorite
from .models import Tag, Ingredient, Recipe, RecipeIngredient


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админка для тегов."""

    list_display = ("id", "name", "slug")
    search_fields = ("name", "slug")
    list_filter = ("name",)
    empty_value_display = "-пусто-"
    list_editable = ("slug",)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админка для ингридиентов."""

    list_display = ("id", "name", "measurement_unit")
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"
    list_editable = ("measurement_unit",)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0
    fk_name = "recipe"


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_display = (
        "id",
        "name",
        "author",
        "cooking_time",
        "created_at",
        "short_link",
        "image",
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin): ...
