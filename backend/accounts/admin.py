from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from unfold.admin import ModelAdmin

from .models import Address, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin, ModelAdmin):
    model = User
    list_display = ["email", "full_name", "phone", "is_active", "is_staff", "date_joined"]
    list_filter = ["is_active", "is_staff"]
    search_fields = ["email", "full_name", "phone"]
    ordering = ["-date_joined"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("بيانات شخصية", {"fields": ("full_name", "phone")}),
        ("الصلاحيات", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )


@admin.register(Address)
class AddressAdmin(ModelAdmin):
    list_display = ["user", "full_name", "city", "is_default"]
    search_fields = ["full_name", "city", "user__email"]
