"""Модуль сериализаторов для модели рецепта."""

from django.utils.translation import gettext_lazy as _
from django.db import transaction
from rest_framework import serializers

from api.v1.serializers import (
    TagSerializer,
    UserSerializer,
)
from api.v1.utils import Base64Field
from cart.models import Cart
from favorite.models import Favorite
from recipes.models import Recipe, Tag, Ingredient, RecipeIngredient


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Класс для сериализации объектов промежуточной модели RecipeIngredient.

    Используется для сериализации ingredients приходящих в POST/PUT запросах.
    Поле id представляет собой объект из queryset модели Ingredient.
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
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit",
    )
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
        request = self.context.get("request", None)
        return bool(
            request is not None
            and request.user.is_authenticated
            and Cart.objects.filter(
                user=request.user,
                recipe=obj,
            ).exists()
        )

    def get_is_favorited(self, obj):
        request = self.context.get("request", None)
        return bool(
            request is not None
            and request.user.is_authenticated
            and Favorite.objects.filter(
                user=request.user,
                recipe=obj,
            ).exists()
        )


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Класс для сериализации рецептов при `POST`/`PUT` запросах."""

    image = Base64Field(required=True, allow_null=False)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
    )
    ingredients = RecipeIngredientSerializer(
        many=True,
        source="recipe_ingredients",
    )
    author = serializers.HiddenField(
        write_only=True,
        default=serializers.CurrentUserDefault(),
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
            "author",
        )

    def validate_image(self, value):
        """Проверяет корректность поля `image`."""
        if not value:
            raise serializers.ValidationError(
                _("Поле image не может быть пустым."),
            )
        return value

    def validate(self, attrs):
        """Переопределяет метод валидации приходящих объектов
        при `POST`/`PUT` запросах."""
        tags = attrs.get("tags")
        ingredients = attrs.get("recipe_ingredients")
        if not tags:
            raise serializers.ValidationError(
                _("Необходимо указать список тегов."),
            )
        tag_ids = [tags.id for tags in tags]
        if len(tag_ids) != len(set(tag_ids)):
            raise serializers.ValidationError(
                _("Теги должны быть уникальными."),
            )
        if not ingredients:
            raise serializers.ValidationError(
                _("Необходимо указать список ингредиентов."),
            )
        ingredient_ids = [
            ingredient["ingredient"].id for ingredient in ingredients
        ]
        if len(ingredient_ids) != len(set(ingredient_ids)):
            raise serializers.ValidationError(
                _("Ингредиенты должны быть уникальными."),
            )
        return super().validate(attrs)

    @transaction.atomic()
    def create(self, validated_data):
        """Переопределяет метод сохранения рецептов при POST-запросах."""
        ingredients_data = validated_data.pop("recipe_ingredients")
        tags = validated_data.pop("tags")
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.bulk_create_recipe_ingredients(
            recipe=recipe,
            ingredients_data=ingredients_data,
        )
        return recipe
    

    @transaction.atomic()
    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop("recipe_ingredients")
        tags = validated_data.pop("tags")
        instance.tags.set(tags)
        instance = super().update(instance, validated_data)
        instance.recipe_ingredients.all().delete()
        self.bulk_create_recipe_ingredients(
            recipe=instance,
            ingredients_data=ingredients_data,
        )
        return instance

    @staticmethod
    def bulk_create_recipe_ingredients(recipe, ingredients_data):
        """Создает объекты `RecipeIngredient` в БД.

        :recipe - Объект рецепта, к которому будут привязаны ингредиенты.
        :ingredients_data - Список ингредиентов для создания объектов.
        """

        RecipeIngredient.objects.bulk_create(
            [
                RecipeIngredient(
                    ingredient=ingredient_data.get("ingredient"),
                    recipe=recipe,
                    amount=ingredient_data.get("amount"),
                )
                for ingredient_data in ingredients_data
            ],
            ignore_conflicts=True,
        )

    def to_representation(self, instance):
        return RecipeReadSerializer(instance, context=self.context).data
