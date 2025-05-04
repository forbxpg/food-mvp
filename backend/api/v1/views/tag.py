"""Модуль для работы с тегами."""

from rest_framework.viewsets import ReadOnlyModelViewSet

from api.v1.serializers import TagSerializer
from recipes.models import Tag


class TagViewSet(ReadOnlyModelViewSet):
    """ViewSet для модели тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
