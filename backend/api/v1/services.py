"""Бизнес-логика API."""

from django.db import transaction
from django.db.utils import IntegrityError

from recipes.models import RecipeIngredient


def bulk_create_recipe_ingredients(recipe, ingredients_data):
    """Создает объекты `RecipeIngredient` в БД.

    :recipe - Объект рецепта, к которому будут привязаны ингредиенты.
    :ingredients_data - Список ингредиентов для создания объектов.
    """
    try:
        with transaction.atomic():
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
    except IntegrityError as e:
        raise IntegrityError(
            "Ошибка при создании объектов RecipeIngredient. "
            "Проверьте, что все ингредиенты существуют в базе данных."
        ) from e
    except Exception as e:
        raise Exception(
            "Ошибка при создании объектов RecipeIngredient."
        ) from e


def get_ingredients_data(cart_items):
    """Получает все ингредиенты в рецептах из списка покупок пользователя."""
    ingredients_data = {}
    for item in cart_items:
        recipe = item.recipe
        recipe_ingredient_data = RecipeIngredient.objects.select_related(
            "recipe",
            "ingredient",
        ).filter(
            recipe=recipe,
        )
        for obj in recipe_ingredient_data:
            name = (
                f"{obj.ingredient.name.capitalize()}"
                f" ({obj.ingredient.measurement_unit})"
            )
            amount = int(obj.amount)
            if name not in ingredients_data:
                ingredients_data[name] = amount
            else:
                ingredients_data[name] += amount
    return ingredients_data


def get_content_for_txt_file(cart):
    """Собирает контент для txt-файла."""
    ingredients_data = get_ingredients_data(cart.cart_items.all())
    content = "  Список покупок \n\n"
    for ingredient, amount in ingredients_data.items():
        content += f"- {ingredient}: {amount}\n"
    return content
