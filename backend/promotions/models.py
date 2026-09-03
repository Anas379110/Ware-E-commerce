from decimal import Decimal

from django.db import models
from django.utils import timezone


class Coupon(models.Model):
    """كوبون خصم (Must — القرار 011). يُطبَّق وقت Checkout فقط، لا يُعاد حسابه بمكان آخر."""

    class DiscountType(models.TextChoices):
        PERCENTAGE = "percentage", "نسبة مئوية"
        FIXED = "fixed", "مبلغ ثابت"

    code = models.CharField(max_length=30, unique=True)
    discount_type = models.CharField(max_length=20, choices=DiscountType.choices)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    usage_limit = models.PositiveIntegerField(null=True, blank=True, help_text="اتركه فارغاً لعدد استخدامات غير محدود")
    times_used = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(discount_value__gt=0), name="coupon_discount_positive")
        ]

    def __str__(self):
        return self.code.upper()

    def is_valid_now(self):
        now = timezone.now()
        if not self.is_active:
            return False, "الكوبون غير مفعَّل."
        if now < self.valid_from or now > self.valid_until:
            return False, "الكوبون منتهي الصلاحية أو لم يبدأ بعد."
        if self.usage_limit is not None and self.times_used >= self.usage_limit:
            return False, "تم استنفاد عدد مرات استخدام هذا الكوبون."
        return True, ""

    def calculate_discount(self, subtotal: Decimal) -> Decimal:
        """يُستدعى فقط بعد التحقق من is_valid_now(). الخصم لا يتجاوز قيمة السلة أبداً."""
        if self.discount_type == self.DiscountType.PERCENTAGE:
            discount = subtotal * (self.discount_value / Decimal("100"))
        else:
            discount = self.discount_value
        return min(discount, subtotal)
