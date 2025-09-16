from django.db import models
from backend.apps.orders.models import Order


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'PENDING'
        SUCCEEDED = 'SUCCEEDED', 'SUCCEEDED'
        FAILED = 'FAILED', 'FAILED'

    provider = models.CharField(max_length=50, default='cinetpay')
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=8, default='XAF')
    reference = models.CharField(max_length=128, blank=True, null=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    idempotency_key = models.CharField(max_length=100, blank=True, null=True)
    raw_response = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
