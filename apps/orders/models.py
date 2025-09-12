from django.conf import settings
from django.db import models
from django.utils import timezone
from backend.apps.catalog.models import Product


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    updated_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')


class PickupSlot(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.PositiveIntegerField(default=20)

    class Meta:
        unique_together = ('date', 'start_time', 'end_time')


class Order(models.Model):
    class Status(models.TextChoices):
        CREATED = 'CREATED', 'CREATED'
        PAID = 'PAID', 'PAID'
        IN_PREPARATION = 'IN_PREPARATION', 'IN_PREPARATION'
        READY_FOR_PICKUP = 'READY_FOR_PICKUP', 'READY_FOR_PICKUP'
        PICKED_UP = 'PICKED_UP', 'PICKED_UP'
        CLOSED = 'CLOSED', 'CLOSED'
        CANCELLED_NOT_COLLECTED = 'CANCELLED_NOT_COLLECTED', 'CANCELLED_NOT_COLLECTED'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.CREATED)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=8, default=getattr(settings, 'CURRENCY', 'XAF'))
    contact_name = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=64)
    contact_email = models.EmailField(blank=True, null=True)
    pickup_date = models.DateField()
    pickup_start = models.TimeField()
    pickup_end = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    line_total = models.DecimalField(max_digits=12, decimal_places=2)
