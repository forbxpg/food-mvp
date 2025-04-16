"""Модуль с ViewSet для ингредиентов."""

from rest_framework import filters

from api.v1.serializers import IngredientSerializer
from api.v1.viewsets import RetrieveListViewSet
from recipes.models import Ingredient


class IngredientViewSet(RetrieveListViewSet):
    """ViewSet для модели ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (
        filters.SearchFilter,  # чувствителен к регистру при использовании SQLite3
    )
    search_fields = ("^name",)
