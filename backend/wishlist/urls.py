from django.urls import path

from .views import WishlistItemDeleteView, WishlistView

urlpatterns = [
    path("", WishlistView.as_view(), name="wishlist-list"),
    path("<int:product_id>", WishlistItemDeleteView.as_view(), name="wishlist-delete"),
]
