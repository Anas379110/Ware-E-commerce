from django.urls import path

from .views import (
    ShamCashInitiateView,
    ShamCashWebhookView,
    StripeCreateSessionView,
    StripeWebhookView,
)

urlpatterns = [
    path("stripe/create-session", StripeCreateSessionView.as_view(), name="stripe-create-session"),
    path("stripe/webhook", StripeWebhookView.as_view(), name="stripe-webhook"),
    path("sham-cash/initiate", ShamCashInitiateView.as_view(), name="sham-cash-initiate"),
    path("sham-cash/webhook", ShamCashWebhookView.as_view(), name="sham-cash-webhook"),
]
