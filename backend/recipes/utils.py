from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class IsFavoriteRecipe(IntegerChoices):
    """Класс для определения статуса рецепта в избранном."""

    YES = 1, _("В избранном")
    NO = 0, _("Не в избранном")


class IsInShoppingCart(IntegerChoices):
    """Класс для определения статуса рецепта в корзине."""

    YES = 1, _("В корзине")
    NO = 0, _("Не в корзине")
