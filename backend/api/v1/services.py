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


def get_ingredients_data(cart_items):
    ingredients_data = {}
    for item in cart_items:
        recipe = item.recipe
        recipe_ingredient_data = RecipeIngredient.objects.select_related(
            "recipe",
            "ingredient",
        ).filter(
            recipe=recipe,
        )
        print(recipe_ingredient_data)
        for obj in recipe_ingredient_data:
            name = f"{obj.ingredient.name.capitalize()} ({obj.ingredient.measurement_unit})"
            amount = int(obj.amount)
            if not name in ingredients_data:
                ingredients_data[name] = amount
            else:
                ingredients_data[name] += amount
    return ingredients_data


def get_content_for_txt_file(cart):
    """Создает текстовый файл с рецептами из списка покупок пользователя."""
    ingredients_data = get_ingredients_data(cart.cart_items.all())
    content = "     Список покупок \n\n"
    for ingredient, amount in ingredients_data.items():
        content += f"   - {ingredient}: {amount}\n"
    return content


def generate_code():
    return secrets.token_urlsafe(config.SHORT_LINK_LENGTH)
