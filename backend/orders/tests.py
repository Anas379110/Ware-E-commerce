from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Address, User
from catalog.models import Category, Product


class CheckoutTests(APITestCase):
    def setUp(self):
        category = Category.objects.create(name="أدوات", slug="tools")
        self.product = Product.objects.create(
            category=category, name="مفك براغي", slug="screwdriver", price=10, stock_quantity=5
        )
        self.user = User.objects.create_user(email="buyer@example.com", password="StrongPass123!")
        self.address = Address.objects.create(
            user=self.user, full_name="زبون", phone="0999999999", city="دمشق", street_details="شارع تجريبي"
        )

        login = self.client.post(
            reverse("auth-login"), {"email": "buyer@example.com", "password": "StrongPass123!"}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")

    def test_checkout_requires_authentication(self):
        self.client.credentials()
        response = self.client.post(reverse("checkout"), {"address_id": self.address.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_checkout_fails_on_empty_cart(self):
        response = self.client.post(reverse("checkout"), {"address_id": self.address.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_checkout_fails_on_invalid_address(self):
        self.client.post(reverse("cart-item-list"), {"product": self.product.id, "quantity": 1})
        response = self.client.post(reverse("checkout"), {"address_id": 9999})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_checkout_fails_when_quantity_exceeds_stock(self):
        # يضاف للسلة بكمية صالحة، ثم يُخفَّض المخزون يدوياً لمحاكاة تغيّر بين الإضافة والدفع
        self.client.post(reverse("cart-item-list"), {"product": self.product.id, "quantity": 3})
        self.product.stock_quantity = 1
        self.product.save(update_fields=["stock_quantity"])

        response = self.client.post(reverse("checkout"), {"address_id": self.address.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_checkout_success_creates_pending_order_without_deducting_stock(self):
        self.client.post(reverse("cart-item-list"), {"product": self.product.id, "quantity": 2})

        response = self.client.post(reverse("checkout"), {"address_id": self.address.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "pending")
        self.assertEqual(str(response.data["total_amount"]), "20.00")

        # مبدأ أمني: لا يُخصَم المخزون إلا بعد تأكيد الدفع عبر Webhook — راجع ARCHITECTURE.md
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_quantity, 5)

        cart_response = self.client.get(reverse("cart-detail"))
        self.assertEqual(len(cart_response.data["items"]), 0)
