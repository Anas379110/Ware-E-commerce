from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Category, Product


class ProductListTests(APITestCase):
    def setUp(self):
        self.cat_a = Category.objects.create(name="أدوات", slug="tools")
        self.cat_b = Category.objects.create(name="معدات", slug="equipment")

        self.active_product = Product.objects.create(
            category=self.cat_a, name="مفك براغي", slug="screwdriver", price=5, stock_quantity=10
        )
        Product.objects.create(
            category=self.cat_a,
            name="منتج مخفي",
            slug="hidden",
            price=5,
            stock_quantity=10,
            is_active=False,
        )
        Product.objects.create(
            category=self.cat_b, name="مولّد كهرباء", slug="generator", price=500, stock_quantity=2
        )

    def test_list_excludes_inactive_products(self):
        response = self.client.get(reverse("product-list"))
        names = [p["name"] for p in response.data["results"]]
        self.assertNotIn("منتج مخفي", names)

    def test_filter_by_category(self):
        response = self.client.get(reverse("product-list"), {"category": "tools"})
        names = [p["name"] for p in response.data["results"]]
        self.assertEqual(names, ["مفك براغي"])

    def test_search_by_name(self):
        response = self.client.get(reverse("product-list"), {"search": "مولّد"})
        names = [p["name"] for p in response.data["results"]]
        self.assertEqual(names, ["مولّد كهرباء"])

    def test_price_filter(self):
        response = self.client.get(reverse("product-list"), {"min_price": 100})
        names = [p["name"] for p in response.data["results"]]
        self.assertEqual(names, ["مولّد كهرباء"])

    def test_product_detail_by_slug(self):
        response = self.client.get(reverse("product-detail", args=["screwdriver"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "مفك براغي")

    def test_inactive_product_detail_returns_404(self):
        response = self.client.get(reverse("product-detail", args=["hidden"]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
