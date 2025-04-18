from rest_framework import serializers

from favorite.models import FavoriteRecipe, Favorite
from recipes.models import Recipe


class FavoriteRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ("id", "image", "cooking_time", "name")


class FavoriteSerializer(serializers.ModelSerializer):

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
