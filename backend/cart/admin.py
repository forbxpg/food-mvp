from django.contrib import admin


from cart.models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    """Inline admin for CartItem model."""

    model = CartItem
    extra = 0
    fields = ("recipe",)
    verbose_name = "Recipe in Cart"
    verbose_name_plural = "Recipes in Cart"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin interface for Cart model."""

    inlines = (CartItemInline,)

    list_display = ("id", "user")
    search_fields = ("user__username",)
    list_filter = ("user__email",)
