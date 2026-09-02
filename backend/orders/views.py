from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Address
from cart.views import get_or_create_cart

from .models import Order, OrderItem
from .serializers import OrderSerializer


class CheckoutView(APIView):
    """POST /api/v1/checkout — UC-01: إنشاء الطلب من السلة الحالية بحالة pending.

    لا يُخصَم المخزون هنا — يُخصَم فقط بعد تأكيد الدفع عبر Webhook موقَّع
    (راجع ARCHITECTURE.md: مبدأ أمان أساسي).
    """

    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        cart = get_or_create_cart(request)
        items = list(cart.items.select_related("product"))
        if not items:
            raise ValidationError({"error": "السلة فارغة — لا يمكن إتمام الشراء."})

        address_id = request.data.get("address_id")
        address = Address.objects.filter(pk=address_id, user=request.user).first()
        if not address:
            raise ValidationError({"error": "عنوان الشحن غير صالح."})

        for item in items:
            if item.quantity > item.product.stock_quantity:
                raise ValidationError(
                    {"error": f"الكمية المطلوبة من '{item.product.name}' تتجاوز المخزون المتوفر."}
                )

        total = sum(item.product.price * item.quantity for item in items)
        order = Order.objects.create(user=request.user, address=address, total_amount=total)

        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    product=item.product,
                    product_name_snapshot=item.product.name,
                    unit_price_snapshot=item.product.price,
                    quantity=item.quantity,
                )
                for item in items
            ]
        )

        cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderListView(generics.ListAPIView):
    """GET /api/v1/orders — طلبات المستخدم الحالي (US-06 من جهة العرض)."""

    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items")


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items")
