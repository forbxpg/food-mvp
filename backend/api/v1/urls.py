"""URLs for the API v1."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import (
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet,
    UserViewSet,
)


v1_router = DefaultRouter()

v1_router.register(
    "tags",
    TagViewSet,
    basename="tags",
)
v1_router.register(
    "users",
    UserViewSet,
    basename="users",
)
v1_router.register(
    "ingredients",
    IngredientViewSet,
    basename="ingredients",
)
v1_router.register(
    "recipes",
    RecipeViewSet,
    basename="recipes",
)


urlpatterns = [
    path("", include(v1_router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
]
