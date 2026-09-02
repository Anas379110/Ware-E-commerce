from django.conf import settings
from django.db import models

from catalog.models import Product


class Cart(models.Model):
    """سلة مرتبطة بمستخدم مسجّل، أو بمفتاح جلسة للزائر (FR-03.3)."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="cart"
    )
    session_key = models.CharField(max_length=64, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"سلة #{self.pk}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ["cart", "product"]
        constraints = [
            models.CheckConstraint(check=models.Q(quantity__gt=0), name="cart_item_quantity_positive")
        ]

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"
