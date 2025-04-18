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


class Subscription(models.Model):
    """Модель подписки пользователя на другого пользователя.

    Используется для хранения информации о подписках пользователей.
    """

    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name=_("Подписчик"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers",
        verbose_name=_("Автор"),
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("subscriber", "author"),
                name="unique_user_author_subscription",
            ),
            models.CheckConstraint(
                check=~models.Q(follower=models.F("user")),
                name="prevent_self_subscription",
                violation_error_message=_("Нельзя подписаться на самого себя."),
            ),
        ]
        verbose_name = _("Подписка")
        verbose_name_plural = _("Подписки")
