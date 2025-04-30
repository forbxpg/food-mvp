from django.contrib import admin

from unfold.admin import ModelAdmin, TabularInline

from cart.models import CartItem, Cart


class CartItemInline(TabularInline):
    model = CartItem
    extra = 0
    fk_name = "cart"
    fields = ("recipe",)


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    inlines = (CartItemInline,)
    fields = ("user",)
