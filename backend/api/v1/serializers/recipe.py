"""Модуль сериализаторов для модели рецепта."""

from rest_framework import serializers

from api.v1.serializers import (
    UserSerializer,
    IngredientSerializer,
    TagSerializer,
)
from recipes.models import Recipe, Tag


class RecipeReadSerializer(serializers.ModelSerializer):

    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "author",
            "text",
            "cooking_time",
            "is_favorited",
            "is_in_shopping_cart",
            "ingredients",
            "tags",
        )


class RecipeWriteSerializer(serializers.ModelSerializer):

    tags = serializers.PrimaryKeyRelatedField(
        many=True, required=True, queryset=Tag.objects.all()
    )
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "author",
            "text",
            "cooking_time",
            "is_favorited",
            "is_in_shopping_cart",
            "tags",
            "ingredients",
        )
        read_only_fields = ("author",)

    def to_representation(self, instance):
        return RecipeWriteSerializer(instance).data
