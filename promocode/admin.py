from django.contrib import admin


class PromoCodeAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "discount_percentage",
        "is_cumulative",
        "valid_from",
        "valid_to",
    )
    search_fields = ("code",)
    ordering = ("code",)