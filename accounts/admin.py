from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "is_active",
        "create_at",
    )
    list_filter = ("is_active", "is_staff", "is_superuser", "create_at")
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("-create_at",)

    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "avatar", "bio")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Important dates",
            {"fields": ("last_login", "date_joined", "create_at", "update_at")},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )

    readonly_fields = ("create_at", "update_at")
