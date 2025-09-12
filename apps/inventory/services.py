from django.db import transaction
from django.db.models import F
from backend.apps.catalog.models import Product
from .models import Inventory, StockMovement


@transaction.atomic
def reserve_stock(product: Product, qty: int) -> bool:
    inv, _ = Inventory.objects.select_for_update().get_or_create(product=product)
    if inv.qty_available < qty:
        return False
    inv.qty_available = F('qty_available') - qty
    inv.save()
    StockMovement.objects.create(product=product, change=-qty, reason='reserve')
    return True


@transaction.atomic
def release_stock(product: Product, qty: int):
    inv, _ = Inventory.objects.select_for_update().get_or_create(product=product)
    inv.qty_available = F('qty_available') + qty
    inv.save()
    StockMovement.objects.create(product=product, change=qty, reason='release')


@transaction.atomic
def adjust_stock(product: Product, delta: int, reason: str):
    inv, _ = Inventory.objects.select_for_update().get_or_create(product=product)
    inv.qty_available = F('qty_available') + delta
    inv.save()
    StockMovement.objects.create(product=product, change=delta, reason=reason)
