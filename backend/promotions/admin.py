from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(ModelAdmin):
    list_display = ["code", "discount_type", "discount_value", "valid_from", "valid_until", "times_used", "usage_limit", "is_active"]
    list_filter = ["discount_type", "is_active"]
    search_fields = ["code"]
    readonly_fields = ["times_used"]

    def save_model(self, request, obj, form, change):
        obj.code = obj.code.upper().strip()
        super().save_model(request, obj, form, change)
