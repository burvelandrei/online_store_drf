from django.contrib import admin
from .models import CartProduct


class CartProductAdmin(admin.ModelAdmin):
    list_display = (
        "cart__id",
        "product",
        "quantity",
        "total_price",
    )
    search_fields = (
        "cart__id",
        "product",
    )
    ordering = ("cart__id",)
    readonly_fields = ("cart_id",)


admin.site.register(CartProduct, CartProductAdmin)
