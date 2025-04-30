"""Модуль представлений для работы с рецептами."""

from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404, redirect
from rest_framework import permissions, status, viewsets, views
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.filters import RecipeFilter
from api.v1.serializers import (
    CartItemSerializer,
    FavoriteSerializer,
    RecipeReadSerializer,
    RecipeWriteSerializer,
)
from api.v1.pagination import BasePageNumberPagination
from api.v1.permissions import IsAuthorOrReadOnly
from cart.models import Cart, CartItem
from favorite.models import Favorite, FavoriteRecipe
from recipes.models import Recipe


RECIPE_ACTIONS_SERIALIZERS_MAPPING = {
    "list": RecipeReadSerializer,
    "retrieve": RecipeReadSerializer,
    "create": RecipeWriteSerializer,
    "update": RecipeWriteSerializer,
    "partial_update": RecipeWriteSerializer,
    "destroy": RecipeWriteSerializer,
    "add_or_delete_recipe_in_shopping_cart": CartItemSerializer,
    "add_or_delete_recipe_in_favorite": FavoriteSerializer,
}


class RecipeViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с рецептами."""

    queryset = Recipe.objects.select_related(
        "author",
    ).prefetch_related(
        "tags",
        "ingredients",
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = BasePageNumberPagination
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in RECIPE_ACTIONS_SERIALIZERS_MAPPING:
            return RECIPE_ACTIONS_SERIALIZERS_MAPPING[self.action]
        return super().get_serializer_class()

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
            serializer = self.get_serializer(
                data={"cart": cart.id, "recipe": recipe.id}
            )
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
            favorite, created = Favorite.objects.get_or_create(
                user=request.user,
            )
            serializer = self.get_serializer(
                data={"recipe": recipe.id, "favorite": favorite.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
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
    def get_short_link_action(self, request, *args, **kwargs):
        """Метод для получения короткой ссылки на рецепт."""
        recipe = self.get_object()
        print(recipe.link)
        return Response(
            data={"short-link": f"{settings.SITE_URL}/f/{recipe.link}"},
            status=status.HTTP_200_OK,
        )


class GetRecipeViaLinkAPIView(views.APIView):
    """APIView для редиректа по короткой ссылке."""

    def get(self, request, short_link):
        recipe = get_object_or_404(
            Recipe,
            link=short_link,
        )
        return redirect(
            f"/recipes/{recipe.id}",
        )
