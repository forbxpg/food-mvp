"""Модуль для роутеров API v1."""

from rest_framework.routers import DefaultRouter

from api.v1.views import (
    TagViewSet,
    IngredientViewSet,
)


v1_router = DefaultRouter()

v1_router.register("tags", TagViewSet, basename="tags")
v1_router.register("ingredients", IngredientViewSet, basename="ingredients")
