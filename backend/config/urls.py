from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("accounts.urls")),
    path("api/v1/account/", include("accounts.account_urls")),
    path("api/v1/", include("catalog.urls")),
    path("api/v1/", include("reviews.urls")),
    path("api/v1/cart/", include("cart.urls")),
    path("api/v1/", include("orders.urls")),
    path("api/v1/payments/", include("payments.urls")),
    path("api/v1/wishlist/", include("wishlist.urls")),
    path("api/v1/promotions/", include("promotions.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
