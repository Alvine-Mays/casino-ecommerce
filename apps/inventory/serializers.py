from rest_framework import serializers
from .models import Inventory


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['product', 'qty_available', 'low_stock_threshold']
        read_only_fields = ['product']
