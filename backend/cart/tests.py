from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from catalog.models import Category, Product


class CartTests(APITestCase):
    def setUp(self):
        category = Category.objects.create(name="أدوات", slug="tools")
        self.product = Product.objects.create(
            category=category, name="مفك براغي", slug="screwdriver", price=5, stock_quantity=3
        )
        self.user = User.objects.create_user(email="buyer@example.com", password="StrongPass123!")

    def authenticate(self):
        login = self.client.post(
            reverse("auth-login"), {"email": "buyer@example.com", "password": "StrongPass123!"}
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")

    def test_guest_can_add_item_to_cart(self):
        response = self.client.post(
            reverse("cart-item-list"), {"product": self.product.id, "quantity": 2}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        cart_response = self.client.get(reverse("cart-detail"))
        self.assertEqual(len(cart_response.data["items"]), 1)
        self.assertEqual(cart_response.data["items"][0]["quantity"], 2)

    def test_authenticated_user_cart_persists(self):
        self.authenticate()
        self.client.post(reverse("cart-item-list"), {"product": self.product.id, "quantity": 1})
        cart_response = self.client.get(reverse("cart-detail"))
        self.assertEqual(len(cart_response.data["items"]), 1)

    def test_cannot_add_quantity_exceeding_stock(self):
        response = self.client.post(
            reverse("cart-item-list"), {"product": self.product.id, "quantity": 99}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_and_remove_item(self):
        add = self.client.post(reverse("cart-item-list"), {"product": self.product.id, "quantity": 1})
        item_id = add.data["id"]

        update = self.client.patch(reverse("cart-item-detail", args=[item_id]), {"quantity": 2})
        self.assertEqual(update.status_code, status.HTTP_200_OK)
        self.assertEqual(update.data["quantity"], 2)

        delete = self.client.delete(reverse("cart-item-detail", args=[item_id]))
        self.assertEqual(delete.status_code, status.HTTP_204_NO_CONTENT)
