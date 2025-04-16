"""Модуль сериализаторов для модели пользователя."""

import base64

from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, SetPasswordSerializer
from rest_framework import serializers

from users.models import User


class UserSetPasswordSerializer(SetPasswordSerializer):
    """Сериализатор для изменения пароля пользователя."""

    def save(self, **kwargs):
        """Метод для изменения пароля пользователя."""
        user = self.context.get("request").user
        user.set_password(self.validated_data["new_password"])
        user.save()


class AvatarBase64Field(serializers.ImageField):
    def to_internal_value(self, data):
        """Метод для преобразования данных аватара в Base64."""

        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f"avatar.{ext}")
        return super().to_internal_value(data)


class UserAvatarSerializer(serializers.ModelSerializer):
    """Сериализатор для аватара пользователя."""

    avatar = AvatarBase64Field(allow_null=True, required=False)

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
