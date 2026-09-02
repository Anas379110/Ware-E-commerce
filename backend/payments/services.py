"""
منطق معالجة تأكيد الدفع — يُستدعى فقط من داخل Webhooks مُتحقَّق من توقيعها.
لا يُستدعى هذا المنطق أبداً من أي مسار يستقبل طلباً مباشراً من الواجهة الأمامية
(راجع ARCHITECTURE.md — مبدأ أمان أساسي غير قابل للتفاوض).
"""
from django.db import transaction
from django.db.models import F

from catalog.models import Product
from notifications.services import send_order_confirmation_email
from orders.models import Order

from .models import Payment


@transaction.atomic
def confirm_payment(payment: Payment):
    """يُستدعى بعد التحقق الناجح من توقيع الـ Webhook فقط."""
    order = payment.order

    if order.status == Order.Status.CONFIRMED:
        return  # منع المعالجة المزدوجة (Idempotency) عند وصول Webhook أكثر من مرة

    payment.status = Payment.Status.SUCCEEDED
    payment.save(update_fields=["status"])

    for item in order.items.select_related("product"):
        Product.objects.filter(pk=item.product_id).update(
            stock_quantity=F("stock_quantity") - item.quantity
        )

    order.status = Order.Status.CONFIRMED
    order.save(update_fields=["status", "updated_at"])

    send_order_confirmation_email(order)


def fail_payment(payment: Payment):
    payment.status = Payment.Status.FAILED
    payment.save(update_fields=["status"])

    order = payment.order
    if order.status == Order.Status.PENDING:
        order.status = Order.Status.FAILED
        order.save(update_fields=["status", "updated_at"])
