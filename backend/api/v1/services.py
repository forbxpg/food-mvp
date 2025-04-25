"""Бизнес-логика API."""

from uuid import uuid4

from django.conf import settings

from recipes.models import RecipeIngredient


from core.config import SHORT_LINK_LENGTH


def generate_short_link():
    """Генерирует короткий слаг для рецепта."""
    short_link = str(uuid4())[:SHORT_LINK_LENGTH]
    return short_link, f"{settings.SITE_URL}/{short_link}"


def bulk_create_recipe_ingredients(recipe, ingredients_data):
    """Создает объекты `RecipeIngredient` в БД.

    :param recipe: Объект рецепта, к которому будут привязаны ингредиенты.
    :param ingredients_data: Список ингредиентов для создания объектов.
    """
    RecipeIngredient.objects.bulk_create(
        [
            RecipeIngredient(
                ingredient=ingredient_data.get("ingredient"),
                recipe=recipe,
                amount=ingredient_data.get("amount"),
            )
            for ingredient_data in ingredients_data
        ]
    )
