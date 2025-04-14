from django.contrib import admin

from .models import Tag, Ingredient


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
