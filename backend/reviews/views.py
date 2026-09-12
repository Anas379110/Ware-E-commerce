from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, get_object_or_404

from catalog.models import Product

from .models import Review
from .serializers import ReviewSerializer


class ProductReviewListCreateView(ListCreateAPIView):
    """GET/POST /api/v1/products/{slug}/reviews — مرتبطة بمنتج واحد عبر الرابط."""

    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_product(self):
        return get_object_or_404(Product, slug=self.kwargs["slug"], is_active=True)

    def get_queryset(self):
        return Review.objects.filter(product=self.get_product()).select_related("user")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["product"] = self.get_product()
        return context
