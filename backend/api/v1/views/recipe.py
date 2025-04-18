"""Модуль представлений для работы с рецептами."""

from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.serializers import (
    RecipeReadSerializer,
    RecipeWriteSerializer,
    CartItemSerializer,
)
from api.v1.services import generate_short_link
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

    @action(
        methods=["post", "delete"],
        detail=True,
        url_path="shopping_cart",
        permission_classes=[
            permissions.AllowAny
        ],  #### SIDNAOKDNASOKDNAOSKDNAKLSDNALSKDNASKLDNASLKDNSALKdlskamdlkasmdlaksadlkmasl;dmal;smd;lasmdl;asm
    )
    def add_recipe_to_shopping_cart(self, request, *args, **kwargs):
        """Дополнительный action для добавления рецепта в корзину."""
        recipe = self.get_object()
        if request.method == "POST":
            cart, created = Cart.objects.get_or_create(user=request.user)
            serializer = CartItemSerializer(data={"cart": cart.id, "recipe": recipe.id})
            serializer.is_valid(raise_exception=True)
            serializer.save(cart=cart, recipe=recipe)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        elif request.method == "DELETE":
            cart_item = get_object_or_404(
                CartItem.objects.select_related(
                    "recipe",
                    "cart__user",
                ),
                cart__user=self.request.user,
                recipe=recipe,
            )
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["get"], detail=True, url_path="get-link")
    def get_short_link_view(self, request, *args, **kwargs):
        """Дополнительный action для получения короткой ссылки на рецепт."""
        short_link, response_short_link = generate_short_link()
        recipe = self.get_object()
        recipe.short_link = short_link
        recipe.save(update_fields=["short_link"])
        return Response(
            {"short_link": response_short_link},
            status=status.HTTP_200_OK,
        )


class RetrieveRecipeViaShortLinkView(generics.RetrieveAPIView):
    """APIView для получения рецепта по короткой ссылке."""

    queryset = Recipe.objects.select_related(
        "author",
    ).prefetch_related(
        "tags",
        "ingredients",
    )
    serializer_class = RecipeReadSerializer

    def get_object(self):
        short_link = self.kwargs.get("short_link")
        return get_object_or_404(
            self.queryset,
            short_link=short_link,
        )
