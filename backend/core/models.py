"""Базовые абстрактные модели приложения."""

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from recipes.models import Recipe

User = get_user_model()


class AbstractUserRecipeModel(models.Model):
    """
    Базовая абстрактная модель для избранного и корзины.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата добавления"),
    )

    class Meta:
        ordering = ("-created",)
        abstract = True
