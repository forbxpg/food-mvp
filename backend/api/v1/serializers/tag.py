"""Модуль сериализаторов для тегов."""

from rest_framework.serializers import ModelSerializer

from recipes.models import Tag


class TagSerializer(ModelSerializer):
    """Сериализатор для модели Tag."""

    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
            "slug",
        )
