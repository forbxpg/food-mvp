"""Модели приложения Users."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from core import config


class User(AbstractUser):
    """Класс, описывающий пользователя в базе данных."""

    first_name = models.CharField(
        _("Имя"),
        max_length=config.USERNAME_LENGTH,
    )
    last_name = models.CharField(
        _("Фамилия"),
        max_length=config.USERNAME_LENGTH,
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

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")
        ordering = ("username",)

    def __str__(self):
        """Возвращает строковое представление пользователя."""
        return f"Пользователь {self.username}"


class Subscription(models.Model):
    """Модель подписки пользователя на другого пользователя.

    Используется для хранения информации о подписках пользователей.
    :subscriber - пользователь, который подписывается.
    :subscribing - пользователь, на которого подписываются.
    """

    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name=_("Подписчик"),
    )
    subscribing = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscribers",
        verbose_name=_("Автор"),
    )
    created_at = models.DateTimeField(
        _("Дата подписки"),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _("Подписка")
        verbose_name_plural = _("Подписки")
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=("subscriber", "subscribing"),
                name="unique_subscriber_subscribing_subscription",
            ),
            models.CheckConstraint(
                check=~models.Q(subscriber=models.F("subscribing")),
                name="prevent_self_subscription",
                violation_error_message=_("Нельзя подписаться на себя."),
            ),
        ]

    def __str__(self):
        """Возвращает строковое представление подписки."""
        return f"{self.subscriber.username} -> {self.subscribing.username}"
