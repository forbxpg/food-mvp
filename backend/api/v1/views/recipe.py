"""Модуль представлений для работы с рецептами."""

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.generics import RetrieveAPIView
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.filters import RecipeFilter
from api.v1.serializers import (
    RecipeReadSerializer,
    RecipeWriteSerializer,
    CartItemSerializer,
    FavoriteSerializer,
)
from api.v1.services import generate_short_link
from api.v1.pagination import BasePageNumberPagination
from api.v1.permissions import IsAuthorOrReadOnly
from cart.models import Cart, CartItem
from favorite.models import Favorite, FavoriteRecipe
from recipes.models import Recipe


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с рецептами."""

    queryset = Recipe.objects.select_related(
        "author",
    ).prefetch_related(
        "tags",
        "ingredients",
    )
    pagination_class = BasePageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorOrReadOnly,)

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
        permission_classes=[permissions.IsAuthenticated],
    )
    def add_or_delete_recipe_in_shopping_cart(self, request, *args, **kwargs):
        """Дополнительный action для добавления рецепта в корзину."""
        recipe = self.get_object()
        if request.method == "POST":
            cart, created = Cart.objects.get_or_create(user=request.user)
            serializer = CartItemSerializer(data={"cart": cart.id, "recipe": recipe.id})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        elif request.method == "DELETE":
            try:
                recipe.cart_items.get(
                    cart__user=request.user,
                    recipe=recipe,
                ).delete()
            except CartItem.DoesNotExist:
                return Response(
                    {"errors": "Recipe not found in shopping cart."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["post", "delete"],
        detail=True,
        url_path="favorite",
        permission_classes=[permissions.IsAuthenticated],
    )
    def add_or_delete_recipe_in_favorite(self, request, *args, **kwargs):
        """Дополнительный action для добавления рецепта в избранное."""
        recipe = self.get_object()
        if request.method == "POST":
            favorite, created = Favorite.objects.get_or_create(user=request.user)
            serializer = FavoriteSerializer(
                data={"recipe": recipe.id, "favorite": favorite.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(recipe=recipe, favorite=favorite)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        elif request.method == "DELETE":
            try:
                recipe.favorites.get(
                    favorite__user=request.user,
                    recipe=recipe,
                ).delete()
            except FavoriteRecipe.DoesNotExist:
                return Response(
                    {"errors": "Recipe not found in favorites."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["get"], detail=True, url_path="get-link")
    def get_short_link_view(self, request, *args, **kwargs):
        """Дополнительный action для получения короткой ссылки на рецепт."""
        short_link, response_short_link = generate_short_link()
        recipe = self.get_object()
        recipe.short_link = short_link
        recipe.save(update_fields=["short_link"])
        return Response(
            {"short-link": response_short_link},
            status=status.HTTP_200_OK,
        )


class RetrieveRecipeViaShortLinkView(RetrieveAPIView):
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
