"""Админка для управления пользователями."""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from unfold.admin import ModelAdmin, TabularInline
from unfold.forms import UserChangeForm, AdminPasswordChangeForm

from cart.models import CartItem
from favorite.models import FavoriteRecipe
from recipes.models import Recipe


User = get_user_model()

admin.site.unregister(Group)


class RecipeInline(TabularInline):
    fk_name = "author"
    model = Recipe
    extra = 0
    fields = (
        "name",
        "cooking_time",
    )


@admin.register(User)
class UserAdmin(UserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserChangeForm
    change_password_form = AdminPasswordChangeForm
    inlines = (RecipeInline,)
    fieldsets = (
        (_("Данные для входа"), {"fields": ("username", "password")}),
        (
            _("Персональная информация"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "avatar",
                )
            },
        ),
        (
            _("Права доступа"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (_("Последний вход"), {"fields": ("last_login",)}),
        (
            _("Активность пользователя на сайте"),
            {
                "fields": (
                    "subscribers_count",
                    "recipes_in_cart",
                    "recipes_in_favorite",
                )
            },
        ),
    )
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
    )

    list_display_links = (
        "username",
        "id",
        "first_name",
        "last_name",
    )
    readonly_fields = (
        "subscribers_count",
        "recipes_in_cart",
        "recipes_in_favorite",
    )

    def subscribers_count(self, obj):
        return obj.subscribers.count()

    def recipes_in_cart(self, obj):
        return (
            CartItem.objects.select_related(
                "cart__user",
                "recipe",
            )
            .filter(cart__user=obj)
            .count()
        )

    def recipes_in_favorite(self, obj):
        return (
            FavoriteRecipe.objects.select_related(
                "favorite__user",
                "recipe",
            )
            .filter(favorite__user=obj)
            .count()
        )

    subscribers_count.short_description = _("Количество подписчиков")
    recipes_in_cart.short_description = _("Рецептов в корзине")
    recipes_in_favorite.short_description = _("Рецептов в избранном")
