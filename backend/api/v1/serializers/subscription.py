"""Модуль сериализаторов для подписок."""

from rest_framework import serializers

from recipes.models import Recipe
from users.models import Subscription


class UserRecipes(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class UserSubscribersSerializer(serializers.ModelSerializer):
    """Сериализатор для подписчика.

    Поля берутся из модели Subscription, но отображаются как поля
    пользователя, на которого подписываются - subscribing.
    """

    id = serializers.IntegerField(source="subscribing.id")
    username = serializers.CharField(source="subscribing.username")
    email = serializers.CharField(source="subscribing.email")
    first_name = serializers.CharField(source="subscribing.first_name")
    last_name = serializers.CharField(source="subscribing.last_name")
    avatar = serializers.ImageField(source="subscribing.avatar")
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "avatar",
            "recipes",
            "recipes_count",
            "is_subscribed",
        )
        model = Subscription

    def get_recipes(self, obj):
        """Получает рецепты subscriber`а."""
        request = self.context.get("request")
        recipes = obj.subscribing.recipes.all()
        recipes_limit = request.query_params.get("recipes_limit")
        if recipes_limit:
            recipes = recipes[: int(recipes_limit)]
        return UserRecipes(recipes, many=True).data

    def get_recipes_count(self, obj):
        """Получает количество рецептов subscriber`а."""
        return obj.subscribing.recipes.count()

    def get_is_subscribed(self, obj):
        """Проверяет подписан ли subscriber на пользователя."""
        request = self.context.get("request")
        return Subscription.objects.filter(
            subscribing=obj.subscribing, subscriber=request.user
        ).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Subscription."""

    class Meta:
        fields = ("id", "subscriber", "subscribing")
        model = Subscription
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=("subscriber", "subscribing"),
                message="Вы уже подписаны на этого пользователя",
            )
        ]

    def validate_subscribing(self, value):
        if value == self.context.get("request").user:
            raise serializers.ValidationError("Нельзя подписаться на себя")
        return value

    def to_representation(self, instance):
        return UserSubscribersSerializer(instance, context=self.context).data
