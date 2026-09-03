from datetime import timedelta
from decimal import Decimal

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Address, User
from catalog.models import Category, Product

from .models import Coupon


class CouponModelTests(APITestCase):
    def test_percentage_discount_calculation(self):
        coupon = Coupon.objects.create(
            code="SAVE10",
            discount_type=Coupon.DiscountType.PERCENTAGE,
            discount_value=Decimal("10"),
            valid_from=timezone.now() - timedelta(days=1),
            valid_until=timezone.now() + timedelta(days=1),
        )
        self.assertEqual(coupon.calculate_discount(Decimal("100")), Decimal("10.00"))

    def test_fixed_discount_never_exceeds_subtotal(self):
        coupon = Coupon.objects.create(
            code="FLAT50",
            discount_type=Coupon.DiscountType.FIXED,
            discount_value=Decimal("50"),
            valid_from=timezone.now() - timedelta(days=1),
            valid_until=timezone.now() + timedelta(days=1),
        )
        self.assertEqual(coupon.calculate_discount(Decimal("20")), Decimal("20"))

    def test_expired_coupon_invalid(self):
        coupon = Coupon.objects.create(
            code="OLD",
            discount_type=Coupon.DiscountType.FIXED,
            discount_value=Decimal("5"),
            valid_from=timezone.now() - timedelta(days=10),
            valid_until=timezone.now() - timedelta(days=1),
        )
        is_valid, _ = coupon.is_valid_now()
        self.assertFalse(is_valid)

    def test_usage_limit_exhausted(self):
        coupon = Coupon.objects.create(
            code="LIMITED",
            discount_type=Coupon.DiscountType.FIXED,
            discount_value=Decimal("5"),
            valid_from=timezone.now() - timedelta(days=1),
            valid_until=timezone.now() + timedelta(days=1),
            usage_limit=1,
            times_used=1,
        )
        is_valid, _ = coupon.is_valid_now()
        self.assertFalse(is_valid)


class CheckoutWithCouponTests(APITestCase):
    def setUp(self):
        category = Category.objects.create(name="أدوات", slug="tools")
        self.product = Product.objects.create(
            category=category, name="مفك براغي", slug="screwdriver", price=100, stock_quantity=5
        )
        self.user = User.objects.create_user(email="buyer@example.com", password="StrongPass123!")
        self.address = Address.objects.create(
            user=self.user, full_name="زبون", phone="0999999999", city="دمشق", street_details="—"
        )
        self.coupon = Coupon.objects.create(
            code="SAVE10",
            discount_type=Coupon.DiscountType.PERCENTAGE,
            discount_value=Decimal("10"),
            valid_from=timezone.now() - timedelta(days=1),
            valid_until=timezone.now() + timedelta(days=1),
        )

        login = self.client.post(
            reverse("auth-login"), {"email": "buyer@example.com", "password": "StrongPass123!"}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")
        self.client.post(reverse("cart-item-list"), {"product": self.product.id, "quantity": 1})

    def test_checkout_applies_valid_coupon(self):
        response = self.client.post(
            reverse("checkout"), {"address_id": self.address.id, "coupon_code": "save10"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(str(response.data["discount_amount"]), "10.00")
        self.assertEqual(str(response.data["total_amount"]), "90.00")

        self.coupon.refresh_from_db()
        self.assertEqual(self.coupon.times_used, 1)

    def test_checkout_rejects_invalid_coupon_code(self):
        response = self.client.post(
            reverse("checkout"), {"address_id": self.address.id, "coupon_code": "NOTREAL"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_checkout_without_coupon_has_zero_discount(self):
        response = self.client.post(reverse("checkout"), {"address_id": self.address.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(str(response.data["discount_amount"]), "0.00")
