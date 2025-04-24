"""Модуль базовых ViewSets."""

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
)


class RetrieveListViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    """
    Базовый ViewSet для получения списка объектов и детальной информации об одном объекте.
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


class CreateDestroyListViewSet(
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    """Базовый ViewSet для создания, удаления и получения списка объектов."""

    ...
