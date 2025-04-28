"""Модели приложения favorites."""

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from recipes.models import Recipe


User = get_user_model()


class FavoriteRecipe(models.Model):
    """Модель для хранения избранных рецептов."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name=_("Рецепт в избранном"),
    )
    favorite = models.ForeignKey(
        "Favorite",
        on_delete=models.CASCADE,
        verbose_name=_("Избранное"),
    )

    class Meta:
        verbose_name = _("Рецепт в избранном")
        verbose_name_plural = _("Избранные рецепты")
        default_related_name = "favorites"
        constraints = [
            models.UniqueConstraint(
                fields=("recipe", "favorite"),
                name="unique_favorite_recipe",
                violation_error_message=_("Этот рецепт уже в избранном."),
            )
        ]

    def __str__(self):
        return f"{self.recipe.name} в избранном {self.favorite.user.username}"


class Favorite(models.Model):
    """Модель избранного пользователя."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Избранное пользователя"),
        related_name="favorite_recipes",
    )

    class Meta:
        verbose_name = _("Избранное")
        verbose_name_plural = _("Избранное")

    def __str__(self):
        return f"Избранное пользователя: {self.user.username}"
