"""Модуль базовых ViewSets."""

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
)


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
