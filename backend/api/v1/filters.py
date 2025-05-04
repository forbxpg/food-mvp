from django_filters import rest_framework as api_filters
from recipes.models import Ingredient, Recipe, Tag


class RecipeFilter(api_filters.FilterSet):
    """Фильтры для рецептов."""

    author = api_filters.CharFilter(
        field_name="author__id",
        lookup_expr="exact",
    )
    tags = api_filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all(),
    )
    is_favorited = api_filters.BooleanFilter(
        field_name="favorites",
        lookup_expr="isnull",
        exclude=True,
    )
    is_in_shopping_cart = api_filters.BooleanFilter(
        field_name="cart_items",
        lookup_expr="isnull",
        exclude=True,
    )

    class Meta:
        model = Recipe
        fields = (
            "author",
            "tags",
            "is_favorited",
            "is_in_shopping_cart",
        )


class IngredientFilter(api_filters.FilterSet):

    name = api_filters.CharFilter(
        field_name="name",
        lookup_expr="startswith",
    )

    class Meta:
        model = Ingredient
        fields = ("name",)
