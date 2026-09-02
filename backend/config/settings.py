"""
Django settings — Ware.
راجع docs/database/DATABASE.md وARCHITECTURE.md قبل أي تعديل هنا.
"""
from datetime import timedelta
from pathlib import Path
import sys
from urllib.parse import urlparse

import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY", default="unsafe-dev-key-change-me")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

INSTALLED_APPS = [
    "unfold",  # لازم قبل django.contrib.admin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    # Ware apps
    "accounts",
    "catalog",
    "cart",
    "orders",
    "payments",
    "notifications",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# --- Database ---
# Use SQLite by default in local development to avoid failing on placeholder values
# such as `postgres://user:pass@host:5432/...` that are common in template env files.
DATABASE_URL = env("DATABASE_URL", default="")
DATABASE_URL_LOWER = DATABASE_URL.lower()
if not DATABASE_URL or ("host" in DATABASE_URL_LOWER and "localhost" not in DATABASE_URL_LOWER and "127.0.0.1" not in DATABASE_URL_LOWER):
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": str(BASE_DIR / "db.sqlite3")}}
else:
    DATABASES = {"default": env.db("DATABASE_URL")}

# --- Redis (Cache / Sessions / Cart) ---
# Redis is optional in local development. If it is not running, fall back to a
# local in-memory cache so API throttling and sessions still work without a
# separate service.
REDIS_URL = env("REDIS_URL", default="redis://localhost:6379/0")
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

try:
    import redis

    client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    client.ping()
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        }
    }
except Exception:
    CACHES["default"] = {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}

# أثناء تشغيل الاختبارات (python manage.py test) لا نتطلب Redis فعلياً —
# نستخدم Cache محلي بالذاكرة بدل django-redis لتفادي الاعتماد على خدمة خارجية
# في بيئة CI أو أي جهاز مطوّر لا يشغّل Redis محلياً وقت الاختبار فقط.
if "test" in sys.argv:
    CACHES["default"] = {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}
    SESSION_ENGINE = "django.contrib.sessions.backends.db"

AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ar"
TIME_ZONE = "Asia/Damascus"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Frontend (Nuxt) ---
FRONTEND_URL = env("FRONTEND_URL", default="http://localhost:3000")

# --- CORS (Nuxt frontend) ---
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=["http://localhost:3000"])
CORS_ALLOW_CREDENTIALS = True

# --- DRF ---
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.ScopedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "auth": "10/min",
        "payments": "20/min",
    },
}

# --- Refresh Token عبر HttpOnly Cookie (إصلاح SECURITY.md — الثغرة #1) ---
# لا يُعاد Refresh Token أبداً بجسم الاستجابة JSON — فقط كـ Cookie لا يصل إليه JavaScript،
# لتقليل أثر أي XSS محتمل بالواجهة الأمامية.
REFRESH_COOKIE_NAME = "ware_refresh_token"
REFRESH_COOKIE_SECURE = env.bool("REFRESH_COOKIE_SECURE", default=not DEBUG)
REFRESH_COOKIE_SAMESITE = env("REFRESH_COOKIE_SAMESITE", default="Lax" if DEBUG else "None")

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# --- Stripe / شام كاش ---
STRIPE_SECRET_KEY = env("STRIPE_SECRET_KEY", default="")
STRIPE_WEBHOOK_SECRET = env("STRIPE_WEBHOOK_SECRET", default="")
SHAM_CASH_API_KEY = env("SHAM_CASH_API_KEY", default="")
SHAM_CASH_WEBHOOK_SECRET = env("SHAM_CASH_WEBHOOK_SECRET", default="")

# --- Email ---
EMAIL_HOST = env("EMAIL_HOST", default="")
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="no-reply@ware.local")

# --- Unfold (لوحة إدارة مخصصة — القرار 009) ---
UNFOLD = {
    "SITE_TITLE": "إدارة Ware",
    "SITE_HEADER": "Ware",
}
