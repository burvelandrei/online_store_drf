from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "role",
        "email",
    )

    search_fields = ("username",)
    ordering = ("username",)

admin.site.register(User, UserAdmin)
