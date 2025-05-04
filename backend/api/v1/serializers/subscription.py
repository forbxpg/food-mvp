"""Модуль сериализаторов для подписок."""

from api.v1.serializers import UserSerializer
from api.v1.utils import BaseRecipeReadSerializer
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from users.models import Subscription

User = get_user_model()


class SubscriptionReadSerializer(UserSerializer):
    """Сериализатор для отображения подписок пользователя."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + (
            "recipes",
            "recipes_count",
        )
        model = User

    def get_recipes_count(self, obj):
        """Метод для получения количества рецептов пользователя."""
        return obj.recipes.count()

    def get_recipes(self, obj):
        """Метод для получения рецептов пользователя."""
        request = self.context.get("request")
        recipes = obj.recipes.all()
        try:
            recipes_limit = int(request.query_params.get("recipes_limit"))
            recipes = recipes[:recipes_limit]
        except (ValueError, TypeError):
            pass
        return BaseRecipeReadSerializer(recipes, many=True).data


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для возможности подписки на пользователя."""

    class Meta:
        fields = ("subscriber", "subscribing")
        model = Subscription
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=("subscriber", "subscribing"),
                message="Вы уже подписаны на этого пользователя",
            )
        ]

    def validate_subscribing(self, value):
        user = self.context.get("request").user
        if value == user:
            raise serializers.ValidationError(_("Нельзя подписаться на себя"))
        return value

    def to_representation(self, instance):
        return SubscriptionReadSerializer(
            instance.subscribing,
            context=self.context,
        ).data
