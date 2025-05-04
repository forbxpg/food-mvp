"""Модуль с ViewSet для ингредиентов."""

from api.v1.filters import IngredientFilter
from api.v1.serializers import IngredientSerializer
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Ingredient
from rest_framework.viewsets import ReadOnlyModelViewSet


class IngredientViewSet(ReadOnlyModelViewSet):
    """ViewSet для модели ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
