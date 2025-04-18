"""Сериализаторы для корзины."""

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from cart.models import Cart, CartItem
from recipes.models import Recipe


class CartRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для корзины."""

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )


class CartItemSerializer(serializers.ModelSerializer):
    """Сериализатор для корзины."""

    class Meta:
        model = CartItem
        fields = ("id", "cart", "recipe")
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=CartItem.objects.all(),
                fields=("cart", "recipe"),
                message=_("Этот рецепт уже в корзине."),
            )
        ]

    def to_representation(self, instance):
        recipe = instance.recipe
        return CartRecipeSerializer(recipe).data
