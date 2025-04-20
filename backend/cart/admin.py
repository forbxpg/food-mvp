from django.contrib import admin

from cart.models import CartItem, Cart


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    fields = ("cart", "recipe")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    fields = ("user",)
