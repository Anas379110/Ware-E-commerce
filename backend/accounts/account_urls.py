from django.urls import path

from .views import AddressDetailView, AddressListCreateView, MeView

urlpatterns = [
    path("me", MeView.as_view(), name="account-me"),
    path("addresses", AddressListCreateView.as_view(), name="address-list"),
    path("addresses/<int:pk>", AddressDetailView.as_view(), name="address-detail"),
]
