"""Модели приложения cart."""

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from recipes.models import Recipe


User = get_user_model()


class CartItem(models.Model):
    """Класс, описывающий модель рецепта в корзине."""

    cart = models.ForeignKey(
        "Cart",
        on_delete=models.CASCADE,
        verbose_name=_("Корзина"),
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name=_("Рецепт в корзине"),
    )

    class Meta:
        default_related_name = "cart_items"
        verbose_name = _("Рецепт в корзине")
        verbose_name_plural = _("Рецепты в корзине")
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "recipe"],
                name="unique_cart_recipe",
            )
        ]

    def __str__(self):
        return f"Рецепт {self.recipe.name} в корзине \
            {self.cart.user.username} ({self.id})"


class Cart(models.Model):
    """Класс, описывающий модель корзины."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Владелец корзины"),
        related_name="cart",
    )

    class Meta:
        verbose_name = _("Корзина")
        verbose_name_plural = _("Корзины")
        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                name="unique_user_cart",
            )
        ]

    def __str__(self):
        return f"Корзина пользователя {self.user.username} ({self.id})"
