from django.conf import settings
from django.db import models

from accounts.models import Address
from catalog.models import Product


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "قيد الانتظار"
        CONFIRMED = "confirmed", "مؤكَّد"
        SHIPPED = "shipped", "تم الشحن"
        DELIVERED = "delivered", "تم التسليم"
        CANCELLED = "cancelled", "ملغى"
        FAILED = "failed", "فشل الدفع"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders")
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name="orders")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    coupon = models.ForeignKey(
        "promotions.Coupon", on_delete=models.SET_NULL, null=True, blank=True, related_name="orders"
    )
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["user"]), models.Index(fields=["status"])]
        ordering = ["-created_at"]

    def __str__(self):
        return f"طلب #{self.pk} — {self.get_status_display()}"

    @property
    def subtotal(self):
        return self.total_amount + self.discount_amount


class OrderItem(models.Model):
    """نسخة ثابتة (Snapshot) من بيانات المنتج وقت الشراء — لا تتأثر بتعديل المنتج لاحقاً."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name_snapshot = models.CharField(max_length=200)
    unit_price_snapshot = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product_name_snapshot} × {self.quantity}"

    @property
    def subtotal(self):
        return self.unit_price_snapshot * self.quantity
