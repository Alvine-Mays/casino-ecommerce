from django.db import models
from django.conf import settings
from backend.apps.catalog.models import Product


class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='inventory')
    qty_available = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=5)

    def __str__(self):
        return f"{self.product.name}: {self.qty_available}"


class StockMovement(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements')
    change = models.IntegerField()
    reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
