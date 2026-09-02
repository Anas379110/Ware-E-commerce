from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    """سجل تدقيق للمدفوعات — للعرض فقط، لا تعديل يدوي لحالة الدفع."""

    list_display = ["id", "order", "provider", "status", "amount", "created_at"]
    list_filter = ["provider", "status"]
    search_fields = ["order__id", "provider_reference_id"]
    readonly_fields = [f.name for f in Payment._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
