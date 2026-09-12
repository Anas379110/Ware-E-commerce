from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.views import get_or_create_cart

from .models import Coupon


class ValidateCouponView(APIView):
    """POST /api/v1/promotions/validate-coupon — {code}.

    يحسب الخصم اعتماداً على سلة المستخدم الفعلية بالخادم — لا يثق أبداً بقيمة
    subtotal لو أُرسلت من العميل، لمنع التلاعب بحساب الخصم.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        code = (request.data.get("code") or "").strip().upper()
        if not code:
            raise ValidationError({"error": "رمز الكوبون مطلوب."})

        coupon = Coupon.objects.filter(code__iexact=code).first()
        if not coupon:
            raise ValidationError({"error": "رمز الكوبون غير صحيح."})

        is_valid, message = coupon.is_valid_now()
        if not is_valid:
            raise ValidationError({"error": message})

        cart = get_or_create_cart(request)
        subtotal = sum(item.product.price * item.quantity for item in cart.items.all())
        if subtotal <= 0:
            raise ValidationError({"error": "السلة فارغة — لا يمكن تطبيق كوبون."})

        discount = coupon.calculate_discount(subtotal)

        return Response(
            {
                "code": coupon.code,
                "subtotal": subtotal,
                "discount": discount,
                "total_after_discount": subtotal - discount,
            }
        )
