from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "discount",
    )
    search_fields = ("name",)
    ordering = ("name",)

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'discount')
        }),
        ('Расширенные параметры', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(Product, ProductAdmin)
