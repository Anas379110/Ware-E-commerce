from rest_framework import permissions, status
from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import WishlistItem
from .serializers import WishlistItemSerializer


class WishlistView(ListCreateAPIView):
    """GET /api/v1/wishlist — قائمة المفضلة. POST — إضافة منتج."""

    serializer_class = WishlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user).select_related("product")


class WishlistItemDeleteView(APIView):
    """DELETE /api/v1/wishlist/{product_id} — إزالة منتج من المفضلة."""

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, product_id):
        item = get_object_or_404(WishlistItem, user=request.user, product_id=product_id)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
