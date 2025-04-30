"""Модуль сериализаторов для ингредиентов."""

from rest_framework.serializers import ModelSerializer

from recipes.models import Ingredient


class IngredientSerializer(ModelSerializer):
    """Сериализатор для модели ингредиентов."""

    class Meta:
        model = Ingredient
        fields = (
            "id",
            "name",
            "measurement_unit",
        )
