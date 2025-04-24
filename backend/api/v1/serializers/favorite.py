"""Сериализаторы для модели избранного."""

from rest_framework import serializers

from favorite.models import FavoriteRecipe
from recipes.models import Recipe


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения рецепта в избранном."""

    class Meta:
        model = Recipe
        fields = ("id", "image", "cooking_time", "name")


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления/удаления рецепта в избранное."""

    class Meta:
        model = FavoriteRecipe
        fields = ("id", "favorite", "recipe")
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=FavoriteRecipe.objects.all(),
                fields=("recipe", "favorite"),
                message="Этот рецепт уже в избранном.",
            )
        ]

    def to_representation(self, instance):
        return FavoriteRecipeSerializer(instance.recipe).data
