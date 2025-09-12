import random
import string
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from .models import WithdrawalCode
from backend.apps.orders.models import Order


def _rand_code(length: int = 6) -> str:
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(random.choice(alphabet) for _ in range(length))


def generate_temp_code(order: Order) -> WithdrawalCode:
    code = _rand_code(8)
    ttl_hours = min(int(getattr(settings, 'POLICY_EXPIRE_NONPERISHABLE_HOURS', 48)), 48)
    expires = timezone.now() + timedelta(hours=ttl_hours)
    wc = WithdrawalCode.objects.create(order=order, kind=WithdrawalCode.Kind.TEMP, code=code, expires_at=expires)
    return wc


def generate_final_code(order: Order) -> WithdrawalCode:
    code = _rand_code(6)
    expires = timezone.now() + timedelta(minutes=30)
    wc = WithdrawalCode.objects.create(order=order, kind=WithdrawalCode.Kind.FINAL, code=code, expires_at=expires)
    return wc


def validate_code(kind: str, code: str) -> WithdrawalCode | None:
    try:
        wc = WithdrawalCode.objects.select_related('order').get(kind=kind, code=code)
    except WithdrawalCode.DoesNotExist:
        return None
    return wc if wc.is_valid() else None
