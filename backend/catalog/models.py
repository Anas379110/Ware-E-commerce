from django.db import models


class Category(models.Model):
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True)
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="اسم أيقونة من مكتبة lucide (مثال: wrench, hammer, cable) — تُعرض بواجهة المتجر بجانب اسم التصنيف.",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["category", "is_active"]),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(price__gte=0), name="product_price_non_negative"),
            models.CheckConstraint(
                check=models.Q(stock_quantity__gte=0), name="product_stock_non_negative"
            ),
        ]

    def __str__(self):
        return self.name

    @property
    def in_stock(self):
        return self.stock_quantity > 0

    def related_products(self, limit=4):
        """منتجات ذات صلة — نفس التصنيف، باستثناء المنتج نفسه (Must — القرار 011)."""
        return (
            Product.objects.filter(category=self.category, is_active=True)
            .exclude(pk=self.pk)
            .select_related("category")
            .prefetch_related("images")[:limit]
        )

    @property
    def average_rating(self):
        agg = self.reviews.aggregate(avg=models.Avg("rating"))
        return round(agg["avg"], 1) if agg["avg"] else None

    @property
    def review_count(self):
        return self.reviews.count()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/%Y/%m/")
    is_primary = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"صورة {self.product.name}"
