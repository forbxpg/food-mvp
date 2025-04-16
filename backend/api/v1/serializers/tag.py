"""Модуль сериализаторов для тегов."""

from rest_framework.serializers import ModelSerializer

from recipes.models import Tag


class TagSerializer(ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
            "slug",
        )
