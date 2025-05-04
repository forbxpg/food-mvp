"""Модуль сериализаторов для тегов."""

from recipes.models import Tag
from rest_framework.serializers import ModelSerializer


class TagSerializer(ModelSerializer):
    """Сериализатор для модели Tag."""

    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
            "slug",
        )
