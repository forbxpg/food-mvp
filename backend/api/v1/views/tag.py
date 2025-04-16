"""Модуль для работы с тегами."""

from rest_framework import permissions

from api.v1.serializers import TagSerializer
from api.v1.viewsets import RetrieveListViewSet
from recipes.models import Tag


class TagViewSet(RetrieveListViewSet):
    """ViewSet для модели тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
