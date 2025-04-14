"""Модуль для роутеров API v1."""

from rest_framework.routers import DefaultRouter

from api.v1.views import TagViewSet

v1_router = DefaultRouter()

v1_router.register("tags", TagViewSet, basename="tags")
