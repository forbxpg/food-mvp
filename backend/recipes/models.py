from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core import config


class Tag(models.Model):
    """Модель тега в базе данных."""

    name = models.CharField(
        _("Название тега"),
        max_length=config.TAG_FIELDS_LENGTHS,
        unique=True,
    )
    slug = models.CharField(
        _("Slug тега"),
        max_length=config.TAG_FIELDS_LENGTHS,
        unique=True,
        db_index=True,  # Индексация slug для быстрого поиска
    )

    class Meta:
        verbose_name = _("Тег")
        verbose_name_plural = _("Теги")
        ordering = ("-name",)

    def __str__(self):
        return f"Тег: {self.name}"


class RecipeIngredient(models.Model):
    """Промежуточная модель для связи рецепта и ингридиента."""

    ingredient = models.ForeignKey("Ingredient", on_delete=models.CASCADE)
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)


class Ingredient(models.Model):
    """Модель ингридиента в базе данных."""

    name = models.CharField(
        _("Название ингридиента"),
        max_length=config.INGREDIENT_NAME_LENGTH,
    )
    measurement_unit = models.CharField(
        _("Единица измерения"),
        max_length=config.MEASUREMENT_UNIT_LENGTH,
    )

    class Meta:
        verbose_name = _("Ингридиент")
        verbose_name_plural = _("Ингридиенты")
        ordering = ("-name",)


class Recipe(models.Model):
    """Модель рецепта в базе данных."""

    name = models.CharField(
        _("Название рецепта"),
        max_length=config.RECIPE_NAME_LENGTH,
    )
    image = models.ImageField(
        _("Изображение рецепта"),
        upload_to="recipes/images/",
    )
    cooking_time = models.PositiveSmallIntegerField(
        _("Время приготовления"),
        validators=[
            MinValueValidator(1),
        ],
    )
    text = models.TextField(
        _("Описание рецепта"),
    )

    ingredients = models.ManyToManyField(
        to=Ingredient,
        through=RecipeIngredient,
        verbose_name=_("Ингридиенты"),
        related_name="recipes",
    )
    tags = models.ManyToManyField(
        to=Tag,
        verbose_name=_("Теги"),
        related_name="recipes",
    )
