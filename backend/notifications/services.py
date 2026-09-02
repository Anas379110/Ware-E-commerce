import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_order_confirmation_email(order):
    """FR-05.6 — إشعار تأكيد الطلب بعد نجاح الدفع فقط."""
    if not settings.EMAIL_HOST:
        logger.info("EMAIL_HOST غير مُهيَّأ — تخطي إرسال بريد التأكيد (بيئة تطوير).")
        return

    subject = f"تأكيد طلبك رقم #{order.id} — Ware"
    message = (
        f"شكراً لطلبك من Ware.\n\n"
        f"رقم الطلب: {order.id}\n"
        f"الإجمالي: {order.total_amount}\n"
        f"الحالة: {order.get_status_display()}\n\n"
        f"سنُبقيك على اطلاع بمستجدات الشحن."
    )
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [order.user.email],
            fail_silently=False,
        )
    except Exception:
        logger.exception("فشل إرسال بريد تأكيد الطلب #%s", order.id)
