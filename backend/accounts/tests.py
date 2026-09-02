from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class RegisterTests(APITestCase):
    def test_register_creates_user(self):
        url = reverse("auth-register")
        response = self.client.post(
            url,
            {"email": "buyer@example.com", "password": "StrongPass123!", "full_name": "زبون"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="buyer@example.com").exists())

    def test_register_rejects_weak_password(self):
        url = reverse("auth-register")
        response = self.client.post(url, {"email": "weak@example.com", "password": "123"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_rejects_duplicate_email(self):
        User.objects.create_user(email="dup@example.com", password="StrongPass123!")
        url = reverse("auth-register")
        response = self.client.post(url, {"email": "dup@example.com", "password": "StrongPass123!"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="buyer@example.com", password="StrongPass123!")

    def test_login_success_returns_access_token_and_sets_httponly_refresh_cookie(self):
        """راجع SECURITY.md — إصلاح الثغرة #1: Refresh Token لا يظهر بجسم الاستجابة إطلاقاً."""
        url = reverse("auth-login")
        response = self.client.post(url, {"email": "buyer@example.com", "password": "StrongPass123!"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertNotIn("refresh", response.data)

        cookie = response.cookies.get("ware_refresh_token")
        self.assertIsNotNone(cookie)
        self.assertTrue(cookie["httponly"])

    def test_refresh_requires_cookie(self):
        url = reverse("auth-refresh")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_flow_issues_new_access_token(self):
        login_url = reverse("auth-login")
        login_response = self.client.post(
            login_url, {"email": "buyer@example.com", "password": "StrongPass123!"}
        )
        # test client يحتفظ تلقائياً بالـ Cookies بين الطلبات بنفس الجلسة
        refresh_response = self.client.post(reverse("auth-refresh"))
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", refresh_response.data)
        self.assertNotEqual(refresh_response.data["access"], "")

    def test_logout_clears_refresh_cookie(self):
        self.client.post(reverse("auth-login"), {"email": "buyer@example.com", "password": "StrongPass123!"})
        response = self.client.post(reverse("auth-logout"))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.cookies.get("ware_refresh_token").value, "")

    def test_login_wrong_password_rejected(self):
        url = reverse("auth-login")
        response = self.client.post(url, {"email": "buyer@example.com", "password": "wrong"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_requires_authentication(self):
        url = reverse("account-me")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
