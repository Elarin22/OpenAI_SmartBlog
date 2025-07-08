from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "email", "ai_usage_count", "date_joined"]
    list_filter = ["date_joined", "is_staff"]

    fieldsets = UserAdmin.fieldsets + (
        ("추가 정보", {"fields": ("profile_img", "bio", "ai_usage_count")}),
    )
