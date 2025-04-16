"""Модуль ViewSet для работы с пользователями."""

from djoser.serializers import UserCreateSerializer
from rest_framework import status, permissions, pagination
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.viewsets import CreateRetrieveListViewSet
from api.v1.serializers import (
    UserSerializer,
    UserAvatarSerializer,
    UserSetPasswordSerializer,
)
from api.v1.pagination import BasePageNumberPagination
from users.models import User


class UserViewSet(CreateRetrieveListViewSet):
    """ViewSet для работы с пользователями."""

    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    pagination_class = BasePageNumberPagination

    def get_serializer_class(self):
        """Метод для получения сериализатора в зависимости от действия."""
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    @action(
        methods=["get"],
        detail=False,
        url_path="me",
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request, *args, **kwargs):
        """Метод для получения информации о текущем пользователе."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["put", "delete"],
        detail=False,
        url_path="me/avatar",
        permission_classes=[permissions.IsAuthenticated],
    )
    def avatar(self, request, *args, **kwargs):
        """Метод для получения и изменения аватара текущего пользователя."""
        serializer = UserAvatarSerializer(request.user, data=request.data)
        if request.method == "PUT":
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    "avatar": request.user.get_avatar_url,
                },
                status=status.HTTP_200_OK,
            )
        elif request.method == "DELETE":
            if request.user.avatar:
                request.user.avatar.delete(save=True)
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["post"],
        url_path="set_password",
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def set_password(self, request, *args, **kwargs):
        """Метод для изменения пароля пользователя."""
        serializer = UserSetPasswordSerializer(
            request.user, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
