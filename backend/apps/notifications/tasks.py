from celery import shared_task
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from backend.apps.orders.models import Order
from backend.apps.notifications.sms import send_sms
from backend.apps.notifications.email import send_email


@shared_task
def send_payment_confirmation(order_id: int, temp_code: str):
    order = Order.objects.get(id=order_id)
    msg = f"Paiement confirmé. Code TEMP: {temp_code}. Conservez-le pour le retrait."
    if order.contact_phone:
        send_sms(order.contact_phone, msg)
    if order.contact_email:
        send_email(order.contact_email, 'Confirmation de commande', msg)


@shared_task
def send_final_code(order_id: int, final_code: str):
    order = Order.objects.get(id=order_id)
    msg = f"Votre commande est prête. Code FINAL: {final_code}. Valable 30 minutes."
    if order.contact_phone:
        send_sms(order.contact_phone, msg)
    if order.contact_email:
        send_email(order.contact_email, 'Code de retrait', msg)


@shared_task
def send_ready_reminder(order_id: int):
    order = Order.objects.get(id=order_id)
    if order.status == Order.Status.READY_FOR_PICKUP:
        msg = "Rappel: votre commande est prête au retrait."
        if order.contact_phone:
            send_sms(order.contact_phone, msg)
        if order.contact_email:
            send_email(order.contact_email, 'Rappel retrait', msg)


@shared_task
def schedule_ready_reminders():
    now = timezone.now()
    cutoff = now - timedelta(hours=24)
    qs = Order.objects.filter(status=Order.Status.READY_FOR_PICKUP, updated_at__lt=cutoff)
    for o in qs:
        send_ready_reminder.delay(o.id)


@shared_task
def auto_cancel_not_collected():
    from backend.apps.inventory.services import release_stock
    now = timezone.now()
    non_perishable_hours = int(getattr(settings, 'POLICY_EXPIRE_NONPERISHABLE_HOURS', 48))
    cutoff = now - timedelta(hours=non_perishable_hours)
    qs = Order.objects.filter(status=Order.Status.READY_FOR_PICKUP, updated_at__lt=cutoff)
    for order in qs:
        # Restituer le stock
        for it in order.items.select_related('product').all():
            if it.product:
                release_stock(it.product, it.quantity)
        order.status = Order.Status.CANCELLED_NOT_COLLECTED
        order.save(update_fields=['status'])
