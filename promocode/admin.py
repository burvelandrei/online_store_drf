from django.contrib import admin
from .models import PromoCode


class PromoCodeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "discount_percentage",
        "is_cumulative",
        "valid_from",
        "valid_to",
    )
    search_fields = ("code",)
    ordering = ("code",)

admin.site.register(PromoCode, PromoCodeAdmin)