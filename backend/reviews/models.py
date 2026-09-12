from django.conf import settings
from django.db import models

from catalog.models import Product


class Review(models.Model):
    """تقييم ومراجعة منتج — مستخدم واحد يقيّم كل منتج مرة واحدة فقط (Must — القرار 011)."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["product", "user"]
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(rating__gte=1) & models.Q(rating__lte=5), name="review_rating_1_to_5"
            )
        ]

    def __str__(self):
        return f"{self.user.email} → {self.product.name} ({self.rating}★)"
