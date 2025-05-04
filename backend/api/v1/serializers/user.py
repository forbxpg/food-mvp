"""Модуль сериализаторов для модели пользователя."""

from api.v1.utils import Base64Field
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from users.models import Subscription

User = get_user_model()


class UserAvatarSerializer(serializers.ModelSerializer):
    """Сериализатор для аватара пользователя."""

    avatar = Base64Field(
        allow_null=True,
        required=True,
        use_url=True,
        allow_empty_file=False,
    )

    class Meta:
        model = User
        fields = ("avatar",)

    def update(self, instance, validated_data):
        """Метод для обновления данных пользователя."""
        if "avatar" in validated_data:
            instance.avatar.delete()
        return super().update(instance, validated_data)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "username",
            "is_subscribed",
            "avatar",
        )

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        return bool(
            request is not None
            and request.user.is_authenticated
            and Subscription.objects.filter(
                subscriber=obj,
                subscribing=request.user,
            ).exists()
        )


class UserCreationSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя."""

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "username",
            "password",
        )
