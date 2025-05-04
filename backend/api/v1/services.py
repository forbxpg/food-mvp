"""Бизнес-логика API."""

from django.db.models import CharField, F, Sum, Value
from django.db.models.functions.text import Concat
from recipes.models import RecipeIngredient


def get_ingredients_data(cart_items):
    """Получает все ингредиенты в рецептах из списка покупок пользователя."""

    recipes = [item.recipe for item in cart_items]
    qs = (
        RecipeIngredient.objects.select_related(
            "recipe",
            "ingredient",
        )
        .filter(
            recipe__in=recipes,
        )
        .values(
            name=Concat(
                F("ingredient__name"),
                Value("("),
                F("ingredient__measurement_unit"),
                Value(")"),
                output_field=CharField(),
            )
        )
    ).annotate(
        total_amount=Sum("amount"),
    )
    return {row["name"]: int(row["total_amount"]) for row in qs}


def get_content_for_txt_file(items):
    """Собирает контент для txt-файла."""
    ingredients_data = get_ingredients_data(items)
    content = "  Список покупок \n\n"
    for ingredient, amount in ingredients_data.items():
        content += f"- {ingredient}: {amount}\n"
    return content
