"""Сериализаторы для модели избранного."""

from api.v1.utils import BaseRecipeReadSerializer
from django.utils.translation import gettext_lazy as _
from favorite.models import Favorite
from rest_framework import serializers


class FavoriteWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления рецепта в избранное."""

    class Meta:
        model = Favorite
        fields = ("user", "recipe")
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=("recipe", "user"),
                message=_("Этот рецепт уже в избранном."),
            )
        ]

    def to_representation(self, instance):
        return BaseRecipeReadSerializer(instance.recipe).data
