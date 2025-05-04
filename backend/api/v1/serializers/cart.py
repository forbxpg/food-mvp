"""Сериализаторы для модели корзины."""

from api.v1.utils import BaseRecipeReadSerializer
from cart.models import Cart
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class CartWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи рецептов в корзину."""

    class Meta:
        model = Cart
        fields = ("user", "recipe")
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Cart.objects.all(),
                fields=("user", "recipe"),
                message=_("Этот рецепт уже есть в корзине."),
            )
        ]

    def to_representation(self, instance):
        return BaseRecipeReadSerializer(instance.recipe).data
