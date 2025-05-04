"""Модуль базовых ViewSets."""

from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.viewsets import GenericViewSet


class CreateRetrieveListViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    """
    Базовый ViewSet для создания, получения списка и деталей объекта.
    """

    ...
