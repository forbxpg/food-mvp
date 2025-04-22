"""Модуль сериализаторов для модели рецепта."""

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from api.v1.serializers import (
    TagSerializer,
    UserSerializer,
)
from api.v1.utils import Base64Field
from api.v1.services import bulk_create_recipe_ingredients
from cart.models import CartItem
from favorite.models import FavoriteRecipe
from recipes.models import Recipe, Tag, Ingredient, RecipeIngredient


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Класс для сериализации объектов промежуточной модели `RecipeIngredient`.

    Используется для сериализации `ingredients` приходящих в POST/PUT запросах.
    Поле `id` представляет собой объект из `queryset` модели `Ingredient`.
    """

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source="ingredient",
    )

    class Meta:
        model = RecipeIngredient
        fields = ("id", "amount")


class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    """Класс для сериализации объектов промежуточной модели `RecipeIngredient`.

    Используется для сериализации `ingredients` для запросов на их получение.
    Поля берутся как поля объектов модели `Ingredient`.
    """

    id = serializers.IntegerField(source="ingredient.id")
    measurement_unit = serializers.CharField(source="ingredient.measurement_unit")
    name = serializers.CharField(source="ingredient.name")

    class Meta:
        model = RecipeIngredient
        fields = (
            "id",
            "amount",
            "measurement_unit",
            "name",
        )


class RecipeReadSerializer(serializers.ModelSerializer):
    """Класс для сериализации рецептов при запросах на их получение."""

    image = Base64Field()
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientReadSerializer(
        many=True, read_only=True, source="recipe_ingredients"
    )
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
            "text",
            "author",
            "ingredients",
            "tags",
            "is_in_shopping_cart",
            "is_favorited",
        )

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get("request").user
        if user and user.is_authenticated:
            return CartItem.objects.filter(cart__user=user, recipe=obj).exists()
        return False

    def get_is_favorited(self, obj):
        user = self.context.get("request").user
        if user and user.is_authenticated:
            return FavoriteRecipe.objects.filter(
                favorite__user=user, recipe=obj
            ).exists()
        return False


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Класс для сериализации рецептов при `POST`/`PUT` запросах."""

    image = Base64Field()
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
    )
    ingredients = RecipeIngredientSerializer(
        many=True,
        source="recipe_ingredients",
    )

    class Meta:
        model = Recipe
        fields = (
            "id",
            "image",
            "name",
            "cooking_time",
            "ingredients",
            "tags",
            "text",
        )

    def validate_ingredients(self, value):
        if len(value) < 1:
            raise serializers.ValidationError(
                _("Список ингредиентов должен содержать хотя бы один элемент.")
            )
        ingredient_ids = [ingredient["ingredient"].id for ingredient in value]
        if len(ingredient_ids) != len(set(ingredient_ids)):
            raise serializers.ValidationError(_("Ингредиенты должны быть уникальными."))
        for ingredient in value:
            if ingredient.get("amount") is None or ingredient.get("amount") <= 0:
                raise serializers.ValidationError(
                    _("Количество ингредиента должно быть больше нуля.")
                )
        return value

    def validate_tags(self, value):
        if len(value) < 1:
            raise serializers.ValidationError(
                _("Список тегов должен содержать хотя бы один элемент.")
            )
        tag_ids = [tag.id for tag in value]
        if len(tag_ids) != len(set(tag_ids)):
            raise serializers.ValidationError(_("Теги должны быть уникальными."))
        return value

    def create(self, validated_data):
        """Переопределяет метод сохранения приходящих объектов при `POST`-запросе.

        :param validated_data: Провалидированный словарь из `POST`-запроса.
        :return: Созданный объект recipe в БД с заполненными `ingredients` и `tags`.
        """
        ingredients_data = validated_data.pop("recipe_ingredients")
        tags = validated_data.pop("tags")
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        bulk_create_recipe_ingredients(recipe=recipe, ingredients_data=ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop("recipe_ingredients", None)
        tags = validated_data.pop("tags", None)
        if tags is None:
            raise serializers.ValidationError(
                _("Необходимо указать список тегов для обновления.")
            )
        if ingredients_data is None:
            raise serializers.ValidationError(
                _("Необходимо указать список ингредиентов для обновления.")
            )
        instance.tags.set(tags)
        instance = super().update(instance, validated_data)
        instance.recipe_ingredients.all().delete()
        bulk_create_recipe_ingredients(
            recipe=instance, ingredients_data=ingredients_data
        )
        return instance

    def to_representation(self, instance):
        return RecipeReadSerializer(instance, context=self.context).data
