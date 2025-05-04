"""Модуль для работы с тегами."""

from api.v1.serializers import TagSerializer
from recipes.models import Tag
from rest_framework.viewsets import ReadOnlyModelViewSet


class TagViewSet(ReadOnlyModelViewSet):
    """ViewSet для модели тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
