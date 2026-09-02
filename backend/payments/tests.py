from unittest.mock import patch

import stripe
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Address, User
from catalog.models import Category, Product
from orders.models import Order, OrderItem

from .models import Payment
from .services import confirm_payment


class ConfirmPaymentServiceTests(APITestCase):
    """اختبار المنطق الأساسي: تأكيد الدفع يُحدَّث الطلب ويخصم المخزون مرة واحدة فقط."""

    def setUp(self):
        category = Category.objects.create(name="أدوات", slug="tools")
        self.product = Product.objects.create(
            category=category, name="مفك براغي", slug="screwdriver", price=10, stock_quantity=5
        )
        self.user = User.objects.create_user(email="buyer@example.com", password="StrongPass123!")
        self.address = Address.objects.create(
            user=self.user, full_name="زبون", phone="0999999999", city="دمشق", street_details="—"
        )
        self.order = Order.objects.create(user=self.user, address=self.address, total_amount=20)
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            product_name_snapshot=self.product.name,
            unit_price_snapshot=self.product.price,
            quantity=2,
        )
        self.payment = Payment.objects.create(
            order=self.order, provider=Payment.Provider.STRIPE, amount=20
        )

    def test_confirm_payment_deducts_stock_and_confirms_order(self):
        confirm_payment(self.payment)

        self.product.refresh_from_db()
        self.order.refresh_from_db()
        self.payment.refresh_from_db()

        self.assertEqual(self.product.stock_quantity, 3)
        self.assertEqual(self.order.status, Order.Status.CONFIRMED)
        self.assertEqual(self.payment.status, Payment.Status.SUCCEEDED)

    def test_confirm_payment_is_idempotent(self):
        """استدعاء Webhook أكثر من مرة (سلوك شائع لدى بوابات الدفع) يجب ألا يخصم المخزون مرتين."""
        confirm_payment(self.payment)
        confirm_payment(self.payment)

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_quantity, 3)  # وليس 1


class StripeWebhookTests(APITestCase):
    def setUp(self):
        category = Category.objects.create(name="أدوات", slug="tools")
        self.product = Product.objects.create(
            category=category, name="مفك براغي", slug="screwdriver", price=10, stock_quantity=5
        )
        self.user = User.objects.create_user(email="buyer@example.com", password="StrongPass123!")
        self.address = Address.objects.create(
            user=self.user, full_name="زبون", phone="0999999999", city="دمشق", street_details="—"
        )
        self.order = Order.objects.create(user=self.user, address=self.address, total_amount=20)
        self.payment = Payment.objects.create(
            order=self.order, provider=Payment.Provider.STRIPE, amount=20, provider_reference_id="sess_123"
        )

    def test_webhook_rejects_invalid_signature(self):
        """مبدأ أمني غير قابل للتفاوض: لا معالجة بدون توقيع صالح (راجع ARCHITECTURE.md)."""
        with patch("stripe.Webhook.construct_event") as mocked:
            mocked.side_effect = stripe.error.SignatureVerificationError("توقيع غير صالح", sig_header="bad")
            response = self.client.post(
                reverse("stripe-webhook"),
                data="{}",
                content_type="application/json",
                HTTP_STRIPE_SIGNATURE="invalid",
            )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.order.refresh_from_db()
        self.assertEqual(self.order.status, Order.Status.PENDING)  # لم يتغيّر شيء

    def test_webhook_confirms_order_on_valid_completed_event(self):
        fake_event = {
            "type": "checkout.session.completed",
            "data": {"object": {"id": "sess_123"}},
        }
        with patch("stripe.Webhook.construct_event", return_value=fake_event):
            response = self.client.post(
                reverse("stripe-webhook"),
                data="{}",
                content_type="application/json",
                HTTP_STRIPE_SIGNATURE="valid",
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.order.refresh_from_db()
        self.assertEqual(self.order.status, Order.Status.CONFIRMED)
