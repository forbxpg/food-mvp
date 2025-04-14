from django.db import models
from django.utils.translation import gettext_lazy as _

from recipes.models import Recipe
from users.models import User


class Cart(models.Model):
    """Модель корзины в базе данных."""

    recipes = models.ManyToManyField(
        Recipe,
        verbose_name=_("Рецепты"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        default_related_name = "cart"
        verbose_name = _("Корзина")

    def __str__(self):
        """Возвращает строковое представление корзины."""
        return f"Корзина пользователя {self.user.username}"
