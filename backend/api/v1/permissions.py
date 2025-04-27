"""Модуль, определяющий права доступа в приложении."""

from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Проверка прав доступа на авторство объекта."""

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or request.user == obj.author
