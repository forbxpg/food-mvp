"""Модели приложения cart."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import AbstractUserRecipeModel


class Cart(AbstractUserRecipeModel):
    """Класс, описывающий модель рецепта в корзине юзера."""

    class Meta(AbstractUserRecipeModel.Meta):
        default_related_name = "cart_items"
        verbose_name = _("Рецепт в корзине")
        verbose_name_plural = _("Рецепты в корзине")
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique_cart_recipe",
                violation_error_message=_("Рецепт уже есть в корзине!"),
            )
        ]

    def __str__(self):
        return _("Рецепт %(rec)s в корзине пользователя %(user)s") % {
            "rec": self.recipe,
            "user": self.user,
        }
