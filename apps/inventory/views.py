from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from backend.apps.catalog.models import Product
from .models import Inventory
from .serializers import InventorySerializer


class StaffInventoryAdjustView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, product_id: int):
        # Expect body: {"delta": int}
        delta = int(request.data.get('delta', 0))
        product = get_object_or_404(Product, id=product_id)
        inv, _ = Inventory.objects.get_or_create(product=product)
        inv.qty_available = inv.qty_available + delta
        inv.save()
        serializer = InventorySerializer(inv)
        return Response(serializer.data, status=status.HTTP_200_OK)
