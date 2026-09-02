from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Address
from .serializers import AddressSerializer, RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    """FR-04.1 — تسجيل حساب جديد. محمي بـ Rate Limiting لمنع إنشاء حسابات آلية."""

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"


def _set_refresh_cookie(response, refresh_token: str):
    """يضع Refresh Token كـ HttpOnly Cookie — لا يصل إليه JavaScript إطلاقاً.

    راجع SECURITY.md — إصلاح الثغرة #1: هذا هو التغيير الجوهري الذي يمنع سرقة
    Refresh Token عبر XSS محتمل بالواجهة الأمامية.
    """
    response.set_cookie(
        settings.REFRESH_COOKIE_NAME,
        refresh_token,
        httponly=True,
        secure=settings.REFRESH_COOKIE_SECURE,
        samesite=settings.REFRESH_COOKIE_SAMESITE,
        max_age=60 * 60 * 24 * 14,  # يطابق REFRESH_TOKEN_LIFETIME
        path="/api/v1/auth/",
    )


class LoginView(APIView):
    """POST /api/v1/auth/login — FR-04.2.

    يُعيد Access Token فقط بجسم الاستجابة، ويضع Refresh Token كـ HttpOnly Cookie.
    """

    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth"

    def post(self, request):
        serializer = TokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = serializer.validated_data

        response = Response({"access": str(tokens["access"])}, status=status.HTTP_200_OK)
        _set_refresh_cookie(response, str(tokens["refresh"]))
        return response


class RefreshView(APIView):
    """POST /api/v1/auth/refresh — يقرأ Refresh Token من الـ Cookie فقط، ليس من الجسم.

    يدعم Rotation: يُصدر Refresh Token جديداً ويستبدل الـ Cookie في كل استدعاء.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        raw_refresh = request.COOKIES.get(settings.REFRESH_COOKIE_NAME)
        if not raw_refresh:
            raise AuthenticationFailed("لا يوجد جلسة نشطة — الرجاء تسجيل الدخول من جديد.")

        serializer = TokenRefreshSerializer(data={"refresh": raw_refresh})
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError:
            raise AuthenticationFailed("الجلسة منتهية — الرجاء تسجيل الدخول من جديد.")

        data = serializer.validated_data
        response = Response({"access": data["access"]}, status=status.HTTP_200_OK)

        new_refresh = data.get("refresh")  # موجود فقط إذا ROTATE_REFRESH_TOKENS=True
        if new_refresh:
            _set_refresh_cookie(response, str(new_refresh))

        return response


class LogoutView(APIView):
    """POST /api/v1/auth/logout — يُبطل Refresh Token الحالي ويحذف الـ Cookie."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        raw_refresh = request.COOKIES.get(settings.REFRESH_COOKIE_NAME)
        if raw_refresh:
            try:
                RefreshToken(raw_refresh).blacklist()
            except Exception:
                pass  # Blacklist app غير مفعّل بعد، أو توكن غير صالح أصلاً — لا يمنع تسجيل الخروج

        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie(settings.REFRESH_COOKIE_NAME, path="/api/v1/auth/")
        return response


class MeView(APIView):
    """FR — بيانات المستخدم الحالي (GET /account/me)."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class AddressListCreateView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)


class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
