"""Модуль представлений для пользователей."""

from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.viewsets import CreateRetrieveListViewSet
from api.v1.pagination import BasePageNumberPagination
from api.v1.serializers import (
    SubscriptionSerializer,
    UserSerializer,
    UserAvatarSerializer,
    UserSetPasswordSerializer,
    UserSubscribersSerializer,
    UserCreationSerializer,
)
from users.models import Subscription


User = get_user_model()

USER_ACTIONS_SERIALIZERS_MAPPING = {
    "create": UserCreationSerializer,
    "list": UserSerializer,
    "retrieve": UserSerializer,
    "current_user_detail_action": UserSerializer,
    "get_subscriptions_list_action": UserSubscribersSerializer,
    "put_or_delete_avatar_action": UserAvatarSerializer,
    "set_password_action": UserSetPasswordSerializer,
    "subscribe_action": SubscriptionSerializer,
}


class UserViewSet(CreateRetrieveListViewSet):
    """ViewSet для создания, получения объекта и списка объектов User."""

    queryset = User.objects.all()
    pagination_class = BasePageNumberPagination

    def get_serializer_class(self):
        """Метод для получения сериализатора в зависимости от действия."""
        if self.action in USER_ACTIONS_SERIALIZERS_MAPPING:
            return USER_ACTIONS_SERIALIZERS_MAPPING[self.action]
        return super().get_serializer_class()

    @action(
        methods=["get"],
        detail=False,
        url_path="me",
        permission_classes=[permissions.IsAuthenticated],
    )
    def current_user_detail_action(self, request, *args, **kwargs):
        """Метод для получения информации о текущем пользователе."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["put", "delete"],
        detail=False,
        url_path="me/avatar",
        permission_classes=[permissions.IsAuthenticated],
    )
    def put_or_delete_avatar_action(self, request, *args, **kwargs):
        """Метод для получения и изменения аватара текущего пользователя."""
        if request.method == "PUT":
            serializer = self.get_serializer(
                request.user,
                data=request.data,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"avatar": request.user.get_avatar_url},
                status=status.HTTP_200_OK,
            )
        elif request.method == "DELETE":
            if request.user.avatar:
                request.user.avatar.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["post"],
        url_path="set_password",
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def set_password_action(self, request, *args, **kwargs):
        """Метод для изменения пароля пользователя."""
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["get"],
        detail=False,
        url_path="subscriptions",
        permission_classes=[permissions.IsAuthenticated],
    )
    def get_subscriptions_list_action(self, request, *args, **kwargs):
        """Метод для получения списка подписок пользователя."""
        user = request.user
        subscriptions_data = user.subscriptions.all()
        page = self.paginate_queryset(subscriptions_data)
        return self.get_paginated_response(
            self.get_serializer(
                page,
                many=True,
                context={"request": request},
            ).data,
        )

    @action(
        methods=["post", "delete"],
        detail=True,
        url_path="subscribe",
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscribe_action(self, request, *args, **kwargs):
        """Метод для подписки на пользователя."""
        subscribing_target = self.get_object()
        user = request.user
        if request.method == "POST":
            serializer = self.get_serializer(
                data={
                    "subscriber": user.id,
                    "subscribing": subscribing_target.id,
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
        elif request.method == "DELETE":
            try:
                user.subscriptions.get(
                    subscribing=subscribing_target,
                    subscriber=user,
                ).delete()
            except Subscription.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_204_NO_CONTENT)
