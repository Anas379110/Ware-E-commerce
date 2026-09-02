from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import Order, OrderItem


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["product", "product_name_snapshot", "unit_price_snapshot", "quantity"]
    can_delete = False


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    """US-06 — إدارة الطلبات: عرض وتغيير الحالة."""

    list_display = ["id", "user", "status", "total_amount", "created_at"]
    list_filter = ["status"]
    search_fields = ["id", "user__email"]
    readonly_fields = ["user", "address", "total_amount", "created_at", "updated_at"]
    inlines = [OrderItemInline]
