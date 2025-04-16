from rest_framework.viewsets import ModelViewSet

from api.v1.serializers import RecipeReadSerializer, RecipeWriteSerializer
from recipes.models import Recipe


class RecipeViewSet(ModelViewSet):
    """ViewSet для модели рецепта."""

    queryset = Recipe.objects.prefetch_related(
        "ingredients",
        "tags",
    ).select_related(
        "author",
    )

    def get_serializer_class(self):
        if self.request.method in ("POST", "PUT"):
            return RecipeWriteSerializer
        return RecipeReadSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return super(RecipeViewSet, self).perform_create(serializer)
