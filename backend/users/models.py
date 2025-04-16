"""Модели приложения Users."""

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


from core import config


class User(AbstractUser):
    """Класс, описывающий пользователя в базе данных."""

    first_name = models.CharField(
        _("Имя"),
        max_length=config.USER_NAME_LENGTH,
    )
    last_name = models.CharField(
        _("Фамилия"),
        max_length=config.USER_NAME_LENGTH,
    )
    email = models.EmailField(
        _("Адрес электронной почты"),
        unique=True,
    )
    avatar = models.ImageField(
        _("Аватар"),
        upload_to="users/",
        blank=True,
        null=True,
    )
    is_subscribed = models.BooleanField(
        _("Подписка"),
        default=False,
    )

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    def __str__(self):
        """Возвращает строковое представление пользователя."""
        return self.username

    @property
    def get_avatar_url(self):
        """Возвращает URL аватара пользователя."""
        if self.avatar:
            return f"{settings.SITE_URL}{self.avatar.url}"
        return None
