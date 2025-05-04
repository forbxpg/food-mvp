"""Утилиты API."""

import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import Recipe


class Base64Field(serializers.ImageField):

    def to_internal_value(self, data):
        """Метод для преобразования данных аватара в Base64."""

        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f"avatar.{ext}")
        return super().to_internal_value(data)


class BaseRecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения рецепта в корзине и избранном."""

    image = Base64Field(
        use_url=True,
        allow_empty_file=False,
        allow_null=False,
        required=True,
    )

    class Meta:
        fields = ("id", "image", "name", "cooking_time")
        model = Recipe
