import logging

import stripe
from django.conf import settings
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from orders.models import Order

from .models import Payment
from .services import confirm_payment, fail_payment

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeCreateSessionView(APIView):
    """POST /api/v1/payments/stripe/create-session — US-03."""

    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "payments"

    def post(self, request):
        order_id = request.data.get("order_id")
        order = Order.objects.filter(pk=order_id, user=request.user, status=Order.Status.PENDING).first()
        if not order:
            raise ValidationError({"error": "طلب غير صالح أو غير قابل للدفع."})

        session = stripe.checkout.Session.create(
            mode="payment",
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": f"طلب Ware #{order.id}"},
                        "unit_amount": int(order.total_amount * 100),
                    },
                    "quantity": 1,
                }
            ],
            metadata={"order_id": str(order.id)},
            success_url=f"{settings.FRONTEND_URL}/orders/{order.id}?status=success",
            cancel_url=f"{settings.FRONTEND_URL}/orders/{order.id}?status=cancelled",
        )

        Payment.objects.create(
            order=order,
            provider=Payment.Provider.STRIPE,
            provider_reference_id=session.id,
            amount=order.total_amount,
        )

        return Response({"checkout_url": session.url})


class StripeWebhookView(APIView):
    """POST /api/v1/payments/stripe/webhook — لا يُستدعى من Nuxt، فقط من Stripe مباشرة.

    مبدأ أمني غير قابل للتفاوض: التحقق من التوقيع قبل أي معالجة.
    """

    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
        except (ValueError, stripe.error.SignatureVerificationError):
            logger.warning("Stripe webhook: توقيع غير صالح — تم رفض الطلب.")
            return Response({"error": "invalid signature"}, status=status.HTTP_400_BAD_REQUEST)

        session = event["data"]["object"]
        payment = Payment.objects.filter(provider_reference_id=session.get("id")).first()
        if not payment:
            logger.warning("Stripe webhook: لم يُعثر على سجل Payment مطابق.")
            return Response(status=status.HTTP_200_OK)

        payment.raw_webhook_payload = event
        payment.save(update_fields=["raw_webhook_payload"])

        if event["type"] == "checkout.session.completed":
            confirm_payment(payment)
        elif event["type"] in ("checkout.session.expired",):
            fail_payment(payment)

        return Response(status=status.HTTP_200_OK)


class ShamCashInitiateView(APIView):
    """POST /api/v1/payments/sham-cash/initiate — US-04 (NEEDS RESEARCH).

    بنية عامة مؤقتة بانتظار توثيق API الرسمي من شام كاش (راجع RESEARCH.md).
    لا تُستخدم هذه الوحدة بإنتاج فعلي قبل استبدال المنطق أدناه بالتكامل الحقيقي.
    """

    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "payments"

    def post(self, request):
        order_id = request.data.get("order_id")
        order = Order.objects.filter(pk=order_id, user=request.user, status=Order.Status.PENDING).first()
        if not order:
            raise ValidationError({"error": "طلب غير صالح أو غير قابل للدفع."})

        if not settings.SHAM_CASH_API_KEY:
            raise ValidationError(
                {"error": "تكامل شام كاش غير مُفعَّل بعد — بانتظار توثيق API الرسمي."}
            )

        # TODO(NEEDS RESEARCH): استبدال هذا القسم بالاستدعاء الفعلي لـ API شام كاش
        # فور استلام التوثيق الرسمي من جهة التواصل.
        payment = Payment.objects.create(
            order=order,
            provider=Payment.Provider.SHAM_CASH,
            amount=order.total_amount,
        )
        return Response(
            {
                "payment_id": payment.id,
                "message": "تكامل شام كاش قيد الإعداد النهائي — بنية عامة مؤقتة.",
            },
            status=status.HTTP_202_ACCEPTED,
        )


class ShamCashWebhookView(APIView):
    """POST /api/v1/payments/sham-cash/webhook — NEEDS RESEARCH.

    يجب أن يتحقق من توقيع شام كاش قبل أي معالجة (نفس مبدأ Stripe Webhook) —
    آلية التوقيع الفعلية غير محددة بعد بانتظار التوثيق الرسمي.
    """

    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        if not settings.SHAM_CASH_WEBHOOK_SECRET:
            logger.error("Sham Cash webhook: SHAM_CASH_WEBHOOK_SECRET غير مُهيَّأ — تم رفض الطلب.")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # TODO(NEEDS RESEARCH): تطبيق التحقق الفعلي من توقيع شام كاش هنا
        # قبل أي استدعاء لـ confirm_payment(). لا يُسمح بتفعيل هذا المسار
        # بإنتاج فعلي قبل إتمام هذا التحقق.
        return Response(
            {"message": "تكامل شام كاش قيد الإعداد النهائي."}, status=status.HTTP_501_NOT_IMPLEMENTED
        )
