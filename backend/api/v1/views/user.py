"""Модуль представлений для пользователей."""

from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.viewsets import CreateRetrieveListViewSet
from api.v1.pagination import BasePageNumberPagination
from api.v1.serializers import (
    SubscriptionSerializer,
    SubscriptionReadSerializer,
    UserSerializer,
    UserAvatarSerializer,
    UserCreationSerializer,
)
from users.models import Subscription


User = get_user_model()

USER_ACTIONS_SERIALIZERS_MAPPING = {
    "create": UserCreationSerializer,
    "list": UserSerializer,
    "retrieve": UserSerializer,
    "me": UserSerializer,
    "subscriptions": SubscriptionSerializer,
    "avatar": UserAvatarSerializer,
    "delete_avatar": UserAvatarSerializer,
    "subscribe": SubscriptionSerializer,
}


class UserViewSet(DjoserUserViewSet):
    """ViewSet для создания, получения объекта и списка объектов User."""

    queryset = User.objects.all()
    pagination_class = BasePageNumberPagination

    def get_permissions(self):
        if self.action in ["create", "list", "retrieve"]:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        """Метод для получения сериализатора в зависимости от действия."""
        if self.action in USER_ACTIONS_SERIALIZERS_MAPPING:
            return USER_ACTIONS_SERIALIZERS_MAPPING[self.action]
        return super().get_serializer_class()

    def get_serializer_context(self):
        """Метод для получения контекста сериализатора."""
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    @action(
        methods=["get"],
        detail=False,
        url_path="me",
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request, *args, **kwargs):
        """Метод для получения информации о текущем пользователе."""
        return super().me(request, *args, **kwargs)

    @action(
        methods=["put"],
        detail=False,
        url_path="me/avatar",
        permission_classes=[permissions.IsAuthenticated],
    )
    def avatar(self, request, *args, **kwargs):
        """Метод для получения и изменения аватара текущего пользователя."""
        serializer = self.get_serializer(
            request.user,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @avatar.mapping.delete
    def delete_avatar(self, request, *args, **kwargs):
        """Метод для удаления аватара текущего пользователя."""
        user = request.user
        if user.avatar:
            user.avatar.delete(save=False)
        user.avatar = None
        user.save()
        serializer = self.get_serializer(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["get"],
        detail=False,
        url_path="subscriptions",
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscriptions(self, request, *args, **kwargs):
        """Метод для получения списка подписок пользователя."""
        subscriptions_data = request.user.subscriptions.all()
        page = self.paginate_queryset(subscriptions_data)
        return self.get_paginated_response(
            self.get_serializer(
                page,
                many=True,
                context={"request": request},
            ).data,
        )

    @action(
        methods=["post"],
        detail=True,
        url_path="subscribe",
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscribe(self, request, *args, **kwargs):
        """Метод для подписки на пользователя."""
        serializer = self.get_serializer(
            data={
                "subscriber": request.user.id,
                "subscribing": self.get_object().id,
            },
            context={
                "request": request,
            },
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @subscribe.mapping.delete
    def delete_subscribe(self, request, *args, **kwargs):
        """Метод для отписки от пользователя."""
        delete_count, dt = Subscription.objects.filter(
            subscriber=request.user,
            subscribing=self.get_object(),
        ).delete()
        if delete_count == 0:
            return Response(
                data={"error": "Вы не подписаны на данного пользователя."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
