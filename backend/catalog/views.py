from django.db.models import Q
from rest_framework import generics, permissions

from .models import Category, Product
from .serializers import CategorySerializer, ProductDetailSerializer, ProductSummarySerializer


class ProductListView(generics.ListAPIView):
    """FR-02.1 / FR-02.3 / FR-02.4 — قائمة المنتجات مع بحث وفلترة."""

    serializer_class = ProductSummarySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True).select_related("category").prefetch_related("images")

        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category__slug=category)

        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(description__icontains=search))

        min_price = self.request.query_params.get("min_price")
        if min_price:
            qs = qs.filter(price__gte=min_price)

        max_price = self.request.query_params.get("max_price")
        if max_price:
            qs = qs.filter(price__lte=max_price)

        return qs.order_by("-created_at")


class ProductDetailView(generics.RetrieveAPIView):
    """FR-02.2 — تفاصيل منتج."""

    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"
    queryset = Product.objects.filter(is_active=True).select_related("category").prefetch_related("images")


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    queryset = Category.objects.filter(is_active=True)
