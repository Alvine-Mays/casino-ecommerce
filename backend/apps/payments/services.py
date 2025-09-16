import logging
from typing import Dict, Any
from django.db import transaction
from django.conf import settings
from backend.apps.orders.models import Order
from backend.apps.payments.models import Payment
import os
from backend.apps.payments.adapters import CinetPayAdapter, MTNMoMoCGAdapter

logger = logging.getLogger(__name__)


def get_adapter(provider: str | None = None):
    prov = (provider or os.getenv('PAYMENT_PROVIDER', 'cinetpay')).lower()
    if prov in ['mtn', 'momo', 'mtn_momo', 'mtn_momo_cg']:
        return MTNMoMoCGAdapter()
    return CinetPayAdapter()


@transaction.atomic
def create_intent(order: Order, provider: str | None = None) -> Dict[str, Any]:
    if hasattr(order, 'payment') and order.payment.status == Payment.Status.SUCCEEDED:
        return {'detail': 'Déjà payé'}
    adapter = get_adapter(provider)
    result = adapter.create_payment_intent(order)
    payment, _ = Payment.objects.get_or_create(order=order, defaults={
        'amount': order.total_amount,
        'currency': order.currency,
        'reference': result.reference,
        'status': Payment.Status.PENDING,
        'raw_response': result.raw,
    })
    payment.reference = result.reference
    payment.raw_response = result.raw
    payment.save()
    return {'reference': result.reference, 'checkout_url': result.checkout_url}


@transaction.atomic
def mark_order_paid(order: Order):
    if order.status != Order.Status.PAID:
        order.status = Order.Status.PAID
        order.save(update_fields=['status'])
        try:
            from backend.apps.pickup.services import generate_temp_code
            from backend.apps.notifications.tasks import send_payment_confirmation
            from backend.apps.orders.utils import broadcast_status
            temp_code = generate_temp_code(order)
            send_payment_confirmation.delay(order.id, temp_code.code)
            broadcast_status(order.id, order.status)
        except Exception as e:
            logger.exception('Post-payment hooks failed: %s', e)


@transaction.atomic
def handle_webhook(payload: Dict[str, Any]):
    reference = payload.get('reference') or payload.get('cpm_trans_id')
    status = payload.get('status') or payload.get('cpm_result')
    payment = Payment.objects.select_for_update().filter(reference=reference).first()
    if not payment:
        logger.warning('Payment not found for reference %s', reference)
        return {'ok': False}
    if status in ['SUCCEEDED', 'ACCEPTED', '00']:
        payment.status = Payment.Status.SUCCEEDED
        payment.save(update_fields=['status'])
        mark_order_paid(payment.order)
        return {'ok': True}
    elif status in ['FAILED', 'REFUSED']:
        payment.status = Payment.Status.FAILED
        payment.save(update_fields=['status'])
        return {'ok': True}
    return {'ok': False}
