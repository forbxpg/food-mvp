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
    is_favorited = api_filters.BooleanFilter(method="filter_user_favorites")
    is_in_shopping_cart = api_filters.BooleanFilter(method="filter_user_cart")

    class Meta:
        model = Recipe
        fields = (
            "author",
            "tags",
            "is_favorited",
            "is_in_shopping_cart",
        )

    def filter_user_favorites(self, queryset, name, value):
        if self.request.user and self.request.user.is_authenticated:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_user_cart(self, queryset, name, value):
        if self.request.user and self.request.user.is_authenticated:
            return queryset.filter(cart_items__user=self.request.user)
        return queryset


class IngredientFilter(api_filters.FilterSet):

    name = api_filters.CharFilter(
        field_name="name",
        lookup_expr="startswith",
    )

    class Meta:
        model = Ingredient
        fields = ("name",)
