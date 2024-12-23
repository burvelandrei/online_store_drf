from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "discount",
    )
    search_fields = ("name",)
    ordering = ("name",)


admin.site.register(Product, ProductAdmin)
