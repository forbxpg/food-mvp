"""Модуль сериализаторов для ингредиентов."""

from recipes.models import Ingredient
from rest_framework.serializers import ModelSerializer


class IngredientSerializer(ModelSerializer):
    """Сериализатор для модели ингредиентов."""

    class Meta:
        model = Ingredient
        fields = (
            "id",
            "name",
            "measurement_unit",
        )
