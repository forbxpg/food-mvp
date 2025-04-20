"""Модуль сериализаторов для модели пользователя."""

from djoser.serializers import SetPasswordSerializer, UserCreateSerializer
from rest_framework import serializers

from api.v1.utils import Base64Field
from users.models import User, Subscription


class UserSetPasswordSerializer(SetPasswordSerializer):
    """Сериализатор для изменения пароля пользователя."""

    def save(self, **kwargs):
        """Метод для изменения пароля пользователя."""
        user = self.context.get("request").user
        user.set_password(self.validated_data["new_password"])
        user.save()


class UserAvatarSerializer(serializers.ModelSerializer):
    """Сериализатор для аватара пользователя."""

    avatar = Base64Field(allow_null=True, required=False)

    class Meta:
        model = User
        fields = ("avatar",)

    def update(self, instance, validated_data):
        """Метод для обновления данных пользователя."""
        if "avatar" in validated_data:
            instance.avatar.delete(save=False)
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
        user = self.context.get("request").user
        return Subscription.objects.filter(
            subscriber=user,
            subscribing=obj,
        ).exists()


class UserCreationSerializer(UserSerializer):
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
