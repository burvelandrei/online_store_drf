from django.contrib import admin
from .models import Cart


class CartAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user__username",
        "created_at",
        "expires_at",
        "total_price",
    )
    search_fields = ("user__username",)
    readonly_fields = (
        "user",
        "created_at",
        "expires_at",
    )
    list_filter = (
        "created_at",
        "expires_at",
    )
    ordering = ("-created_at",)


admin.site.register(Cart, CartAdmin)
