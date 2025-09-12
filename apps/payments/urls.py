from django.urls import path
from .views import CreatePaymentIntentView, PaymentWebhookView

urlpatterns = [
    path('intent', CreatePaymentIntentView.as_view(), name='payments_intent'),
    path('webhook', PaymentWebhookView.as_view(), name='payments_webhook'),
]
