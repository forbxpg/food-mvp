"""Модуль для работы с тегами."""

from api.v1.serializers import TagSerializer
from api.v1.viewsets import RetrieveListViewSet
from recipes.models import Tag


class TagViewSet(RetrieveListViewSet):
    """ViewSet для модели тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
