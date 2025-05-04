"""Модуль представлений для работы с рецептами."""

from django.conf import settings
from django.http.response import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from rest_framework import permissions, status, viewsets, views
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.filters import RecipeFilter
from api.v1.serializers import (
    CartWriteSerializer,
    FavoriteWriteSerializer,
    RecipeReadSerializer,
    RecipeWriteSerializer,
)
from api.v1.pagination import BasePageNumberPagination
from api.v1.permissions import IsAuthorOrReadOnly
from api.v1.services import get_content_for_txt_file
from cart.models import Cart
from favorite.models import Favorite
from recipes.models import Recipe


RECIPE_ACTIONS_SERIALIZERS_MAPPING = {
    "list": RecipeReadSerializer,
    "retrieve": RecipeReadSerializer,
    "create": RecipeWriteSerializer,
    "update": RecipeWriteSerializer,
    "partial_update": RecipeWriteSerializer,
    "destroy": RecipeWriteSerializer,
    "shopping_cart": CartWriteSerializer,
    "favorite": FavoriteWriteSerializer,
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

    def get_serializer_class(self):
        if self.action in RECIPE_ACTIONS_SERIALIZERS_MAPPING:
            return RECIPE_ACTIONS_SERIALIZERS_MAPPING[self.action]
        return super().get_serializer_class()

    def perform_destroy(self, instance):
        if instance.image:
            instance.image.delete(save=False)
        return super().perform_destroy(instance)

    @action(
        methods=["post"],
        detail=True,
        url_path="shopping_cart",
        permission_classes=[permissions.IsAuthenticated],
    )
    def shopping_cart(self, request, *args, **kwargs):
        """Action для добавления рецепта в корзину."""
        serializer = self.get_serializer(
            data={"recipe": self.get_object().id, "user": request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, *args, **kwargs):
        """Action для удаления рецепта в корзине пользователя."""
        delete_count, dt = Cart.objects.filter(
            recipe=self.get_object(),
            user=request.user,
        ).delete()
        if delete_count == 0:
            return Response(
                data={"error": _("Данного рецепта нет в корзине")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["post"],
        detail=True,
        url_path="favorite",
        permission_classes=[permissions.IsAuthenticated],
    )
    def favorite(self, request, *args, **kwargs):
        """Action для добавления рецепта в избранное."""
        serializer = self.get_serializer(
            data={"recipe": self.get_object().id, "user": request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, *args, **kwargs):
        """Action для удаления рецепта из избранного."""
        delete_count, dt = Favorite.objects.filter(
            recipe=self.get_object(),
            user=request.user,
        ).delete()
        if delete_count == 0:
            return Response(
                data={"error": _("Данного рецепта нет в избранном")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["get"], detail=True, url_path="get-link")
    def get_short_link_action(self, request, *args, **kwargs):
        """Метод для получения короткой ссылки на рецепт."""
        return Response(
            data={
                "short-link": f"{settings.SITE_URL}/f/{self.get_object().link}",
            },
            status=status.HTTP_200_OK,
        )

    @action(
        methods=["get"],
        detail=False,
        url_path="download_shopping_cart",
        permission_classes=[permissions.IsAuthenticated],
    )
    def download_shopping_cart(self, request, *args, **kwargs):
        """Action для скачивания списка покупок."""
        content = get_content_for_txt_file(request.user.cart_items.all())
        response = HttpResponse(content, content_type="text/plain")
        response["Content-Disposition"] = 'attachment; filename="list"'
        return response


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
