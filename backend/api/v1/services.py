"""Бизнес-логика API."""

import secrets

from core import config
from recipes.models import RecipeIngredient


def bulk_create_recipe_ingredients(recipe, ingredients_data):
    """Создает объекты `RecipeIngredient` в БД.

    :recipe - Объект рецепта, к которому будут привязаны ингредиенты.
    :ingredients_data - Список ингредиентов для создания объектов.
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


def get_recipes_for_txt_file(user):
    """Создает текстовый файл с рецептами из списка покупок пользователя."""
    content = "Список покупок: \n\n"
    for num, item in enumerate(user.cart_items.all()):
        num += 1
        recipe = item.recipe
        content += f"{num}. {recipe.name}:\n"
        content += f"    Ингредиенты:\n"
        recipe_ingredient_data = RecipeIngredient.objects.select_related(
            "recipe", "ingredient"
        ).filter(recipe=recipe)
        for obj in recipe_ingredient_data:
            content += f"      - {obj.ingredient.name} – {obj.amount} {obj.ingredient.measurement_unit}.\n"
    return content


def generate_code():
    return secrets.token_urlsafe(config.SHORT_LINK_LENGTH)
