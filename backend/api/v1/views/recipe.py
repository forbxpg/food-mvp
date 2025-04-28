"""Модуль представлений для работы с рецептами."""

from django.shortcuts import get_object_or_404, redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets, views
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.filters import RecipeFilter
from api.v1.serializers import (
    CartItemSerializer,
    FavoriteSerializer,
    RecipeReadSerializer,
    RecipeWriteSerializer,
    ShortLinkSerializer,
)
from api.v1.services import generate_code
from api.v1.pagination import BasePageNumberPagination
from api.v1.permissions import IsAuthorOrReadOnly
from cart.models import Cart, CartItem
from favorite.models import Favorite, FavoriteRecipe
from recipes.models import Recipe, ShortLink


RECIPE_ACTIONS_SERIALIZERS_MAPPING = {
    "list": RecipeReadSerializer,
    "retrieve": RecipeReadSerializer,
    "create": RecipeWriteSerializer,
    "update": RecipeWriteSerializer,
    "partial_update": RecipeWriteSerializer,
    "destroy": RecipeWriteSerializer,
    "add_or_delete_recipe_in_shopping_cart": CartItemSerializer,
    "add_or_delete_recipe_in_favorite": FavoriteSerializer,
    "get_short_link_action": ShortLinkSerializer,
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
        try:
            short_link = ShortLink.objects.get(
                recipe_id=kwargs["pk"],
            )
        except ShortLink.DoesNotExist:
            short_code = generate_code()
            while ShortLink.objects.filter(
                short_link=short_code,
            ).exists():
                short_code = generate_code()
            short_link = ShortLink.objects.create(
                recipe_id=kwargs["pk"],
                short_link=short_code,
            )
        serializer = self.get_serializer(short_link)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class GetRecipeViaLinkAPIView(views.APIView):
    """APIView для редиректа по короткой ссылке."""

    def get(self, request, short_link):
        short_link_obj = get_object_or_404(
            ShortLink,
            short_link=short_link,
        )
        recipe_id = short_link_obj.recipe_id
        return redirect(f"/recipes/{recipe_id}")
