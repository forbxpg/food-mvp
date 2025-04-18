"""Модуль сериализаторов для модели подписок."""

from rest_framework import serializers

from api.v1.serializers import UserSerializer
from users.models import Subscription, User


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор модели подписок."""

    user = UserSerializer(source="followers")
    follower = UserSerializer(source="subscriptions")

    class Meta:
        model = Subscription
        fields = ("user", "follower", "id")


class UserSubscriptionsReadSerializer(serializers.ModelSerializer):
    """Сериализатор модели подписок текущего пользователя."""

    subscriptions = SubscriptionSerializer(
        source="subscriptions",
        many=True,
    )
    id = serializers.IntegerField(source="subscriptions.id")
    email = serializers.EmailField(source="subscriptions.email")
    username = serializers.CharField(source="subscriptions.username")
    first_name = serializers.CharField(source="subscriptions.first_name")
    last_name = serializers.CharField(source="subscriptions.last_name")
    is_subscribed = serializers.BooleanField(source="subscriptions.is_subscribed")

    class Meta:
        model = User
        fields = ("id", "email", "username", "first_name", "last_name", "is_subscribed")
