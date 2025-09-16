from rest_framework import permissions, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import F
from backend.apps.catalog.models import Product
from .models import Inventory
from .serializers import InventorySerializer
from backend.apps.accounts.permissions import IsStaffRole


class StaffInventoryListView(generics.ListAPIView):
    """Liste paginée des stocks avec info produit (nom)."""
    permission_classes = [IsStaffRole]
    serializer_class = InventorySerializer

    def get_queryset(self):
        # S'assure que chaque produit a une ligne d'inventaire
        Product.objects.filter(inventory__isnull=True).values_list('id', flat=True)
        qs = Inventory.objects.select_related('product').all().order_by('product__name')
        return qs

    def list(self, request, *args, **kwargs):
        resp = super().list(request, *args, **kwargs)
        # Ajoute le nom du produit pour l'affichage staff
        for item in resp.data.get('results', resp.data if isinstance(resp.data, list) else []):
            try:
                inv = Inventory.objects.select_related('product').get(product_id=item.get('product'))
                item['product_id'] = inv.product_id
                item['product_name'] = inv.product.name
            except Exception:
                pass
        return resp


class StaffInventoryAdjustView(APIView):
    permission_classes = [IsStaffRole]

    def patch(self, request, product_id: int):
        # Body attendu: {"delta": int}
        delta = int(request.data.get('delta', 0))
        product = get_object_or_404(Product, id=product_id)
        inv, _ = Inventory.objects.get_or_create(product=product)
        inv.qty_available = inv.qty_available + delta
        inv.save()
        serializer = InventorySerializer(inv)
        return Response(serializer.data, status=status.HTTP_200_OK)
