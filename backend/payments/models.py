from django.db import models

from orders.models import Order


class Payment(models.Model):
    class Provider(models.TextChoices):
        STRIPE = "stripe", "Stripe"
        SHAM_CASH = "sham_cash", "شام كاش"

    class Status(models.TextChoices):
        PENDING = "pending", "قيد الانتظار"
        SUCCEEDED = "succeeded", "ناجح"
        FAILED = "failed", "فاشل"

    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="payments")
    provider = models.CharField(max_length=20, choices=Provider.choices)
    provider_reference_id = models.CharField(max_length=255, blank=True, db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    raw_webhook_payload = models.JSONField(null=True, blank=True, help_text="للتدقيق فقط — لا يُستخدم بمنطق العمل")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["order"]), models.Index(fields=["provider_reference_id"])]

    def __str__(self):
        return f"دفعة #{self.pk} — {self.get_provider_display()} — {self.get_status_display()}"
