"""Модуль базовых ViewSets."""

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
)


class RetrieveListViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    """
    Базовый ViewSet для получения списка объектов
    и детальной информации об одном объекте.
    """

    ...


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
