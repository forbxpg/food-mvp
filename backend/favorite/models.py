"""Модели приложения favorites."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import AbstractUserRecipeModel


class Favorite(AbstractUserRecipeModel):
    """Модель для хранения избранных рецептов пользователей."""

    class Meta(AbstractUserRecipeModel.Meta):
        verbose_name = _("Рецепт в избранном")
        verbose_name_plural = _("Избранные рецепты")
        default_related_name = "favorites"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"],
                name="unique_favorite_recipe",
                violation_error_message=_("Рецепт уже в избранном!"),
            )
        ]

    def __str__(self):
        return _("Рецепт %(rec)s в избранном пользователя %(user)s") % {
            "rec": self.recipe,
            "user": self.user,
        }
