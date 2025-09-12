from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from backend.apps.accounts.permissions import IsStaffRole
from .models import Order
from .serializers import OrderSerializer
from .utils import broadcast_status


class StaffOrdersListView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsStaffRole]
    serializer_class = OrderSerializer

    def get_queryset(self):
        status_q = self.request.query_params.get('status')
        qs = Order.objects.all().order_by('-created_at')
        if status_q:
            qs = qs.filter(status=status_q)
        return qs


class StaffOrderPrepareView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStaffRole]

    def patch(self, request, order_id: int):
        order = get_object_or_404(Order, id=order_id)
        order.status = Order.Status.IN_PREPARATION
        order.save(update_fields=['status'])
        broadcast_status(order.id, order.status)
        return Response({'status': order.status})


class StaffOrderReadyView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStaffRole]

    def patch(self, request, order_id: int):
        order = get_object_or_404(Order, id=order_id)
        order.status = Order.Status.READY_FOR_PICKUP
        order.save(update_fields=['status'])
        broadcast_status(order.id, order.status)
        return Response({'status': order.status})


class StaffOrderHandoverView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStaffRole]

    def patch(self, request, order_id: int):
        order = get_object_or_404(Order, id=order_id)
        order.status = Order.Status.PICKED_UP
        order.save(update_fields=['status'])
        broadcast_status(order.id, order.status)
        return Response({'status': order.status})
