"""Модуль представлений для работы с рецептами."""

from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.serializers import (
    RecipeReadSerializer,
    RecipeWriteSerializer,
    CartItemSerializer,
)
from cart.models import Cart, CartItem
from recipes.models import Recipe


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с рецептами."""

    queryset = Recipe.objects.select_related(
        "author",
    ).prefetch_related(
        "tags",
        "ingredients",
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RecipeReadSerializer
        return RecipeWriteSerializer

    @action(methods=["post", "delete"], detail=True, url_path="shopping_cart")
    def add_recipe_to_shopping_cart(self, request, *args, **kwargs):
        """Дополнительный action для добавления рецепта в корзину."""
        recipe = self.get_object()
        if request.method == "POST":
            cart, created = Cart.objects.get_or_create(user=request.user)
            serializer = CartItemSerializer(
                data={
                    "cart": cart.id,
                    "recipe": recipe.id,
                },
                context=self.get_serializer_context(),
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(cart=cart, recipe=recipe)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        elif request.method == "DELETE":
            cart = get_object_or_404(
                Cart.objects.select_related("user"),
                user=request.user,
            )
            cart_item = get_object_or_404(
                CartItem,
                cart=cart,
                recipe=recipe,
            )
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
