"""Модели приложения recipes."""

from random import choice
from string import ascii_letters, digits

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import Truncator

from core import config


User = get_user_model()


class Tag(models.Model):
    """Модель тега в базе данных."""

    name = models.CharField(
        _("Название тега"),
        max_length=config.TAG_FIELDS_LENGTHS,
        unique=True,
    )
    slug = models.SlugField(
        _("Идентификатор тега"),
        max_length=config.TAG_FIELDS_LENGTHS,
        unique=True,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Тег")
        verbose_name_plural = _("Теги")
        ordering = ("name",)

    def __str__(self):
        return f"Тег: {self.name}"


class RecipeIngredient(models.Model):
    """Промежуточная модель для связи рецепта и ингредиента."""

    ingredient = models.ForeignKey(
        "Ingredient",
        on_delete=models.CASCADE,
        verbose_name=_("Ингредиент"),
    )
    recipe = models.ForeignKey(
        "Recipe",
        on_delete=models.CASCADE,
        verbose_name=_("Рецепт"),
    )
    amount = models.PositiveSmallIntegerField(
        _("Количество ингредиента"),
        validators=[
            MinValueValidator(
                1,
                message=_("Количество должно быть больше нуля."),
            ),
        ],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("recipe", "ingredient"),
                name="unique_recipe_ingredient",
            )
        ]
        default_related_name = "recipe_ingredients"
        verbose_name = _("Ингредиент в рецепте")
        verbose_name_plural = _("Ингредиенты в рецепте")

    def __str__(self):
        """Возвращает строковое представление ингредиента в рецепте."""
        return f"{self.recipe}: {self.ingredient.name} ({self.amount}"


class Ingredient(models.Model):
    """Модель ингредиента в базе данных."""

    name = models.CharField(
        _("Название ингредиента"),
        max_length=config.INGREDIENT_NAME_LENGTH,
        unique=True,
        db_index=True,
    )
    measurement_unit = models.CharField(
        _("Единица измерения"),
        max_length=config.MEASUREMENT_UNIT_LENGTH,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Ингредиент")
        verbose_name_plural = _("Ингредиенты")
        ordering = ("name",)

    def __str__(self):
        return Truncator(
            f"Ингридиент: {self.name}",
        ).words(
            config.MAX_WORD_TRUNCATOR,
        )


class Recipe(models.Model):
    """Модель рецепта в базе данных."""

    name = models.CharField(
        _("Название рецепта"),
        max_length=config.RECIPE_NAME_LENGTH,
        db_index=True,
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
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Автор рецепта"),
    )
    ingredients = models.ManyToManyField(
        to=Ingredient,
        through=RecipeIngredient,
        verbose_name=_("Ингредиенты"),
    )
    tags = models.ManyToManyField(
        to=Tag,
        verbose_name=_("Теги"),
    )
    created_at = models.DateTimeField(
        _("Добавлено"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("Обновлено"),
        auto_now=True,
    )
    link = models.CharField(
        _("Короткая ссылка для рецепта"),
        max_length=config.SHORT_LINK_LENGTH,
        unique=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Рецепт")
        verbose_name_plural = _("Рецепты")
        ordering = ("-created_at",)
        default_related_name = "recipes"

    def __str__(self):
        """Возвращает строковое представление рецепта."""
        return Truncator(
            f"Рецепт: {self.name}",
        ).words(
            config.MAX_WORD_TRUNCATOR,
        )

    def save(self, *args, **kwargs):
        if self.pk:
            old_img = Recipe.objects.get(pk=self.pk).image
            if old_img and old_img != self.image:
                old_img.delete(save=False)
        if not self.link:
            code = "".join(
                choice(
                    ascii_letters + digits
                ) for _ in range(config.SHORT_LINK_LENGTH)
            )
            while not Recipe.objects.filter(link=code).exists():
                self.link = code
                break
        return super().save(*args, **kwargs)
