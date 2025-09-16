import random
import string
from datetime import timedelta
from django.db import models
from django.utils import timezone
from backend.apps.orders.models import Order


class WithdrawalCode(models.Model):
    class Kind(models.TextChoices):
        TEMP = 'TEMP', 'TEMP'
        FINAL = 'FINAL', 'FINAL'

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='withdrawal_codes')
    kind = models.CharField(max_length=8, choices=Kind.choices)
    code = models.CharField(max_length=16, unique=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        now = timezone.now()
        return (self.used_at is None) and (now < self.expires_at)
