from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from backend.apps.accounts.permissions import IsStaffRole
from backend.apps.inventory.models import Inventory
from backend.apps.catalog.models import Product
from .models import Order, OrderItem
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


class StaffStatsOverviewView(APIView):
    """Aperçu des stats: compte par statut, revenu total (payés+), commandes du jour."""
    permission_classes = [permissions.IsAuthenticated, IsStaffRole]

    def get(self, request):
        statuses = [s[0] for s in Order.Status.choices]
        counts = {s: Order.objects.filter(status=s).count() for s in statuses}
        paid_like = [Order.Status.PAID, Order.Status.IN_PREPARATION, Order.Status.READY_FOR_PICKUP, Order.Status.PICKED_UP, Order.Status.CLOSED]
        revenue = OrderItem.objects.filter(order__status__in=paid_like).aggregate(total=Sum('line_total'))['total'] or 0
        today = timezone.now().date()
        today_orders = Order.objects.filter(created_at__date=today).count()
        return Response({
            'counts': counts,
            'total_revenue': revenue,
            'today_orders': today_orders,
        })


class StaffStatsDailyView(APIView):
    """Séries quotidiennes (commandes & revenu) sur N jours (par défaut 7)."""
    permission_classes = [permissions.IsAuthenticated, IsStaffRole]

    def get(self, request):
        days = int(request.query_params.get('days', '7'))
        since = timezone.now().date() - timezone.timedelta(days=days-1)
        paid_like = [Order.Status.PAID, Order.Status.IN_PREPARATION, Order.Status.READY_FOR_PICKUP, Order.Status.PICKED_UP, Order.Status.CLOSED]
        orders_qs = Order.objects.filter(created_at__date__gte=since)
        revenue_qs = OrderItem.objects.filter(order__status__in=paid_like, order__created_at__date__gte=since)
        orders_series = orders_qs.annotate(d=TruncDate('created_at')).values('d').annotate(count=Count('id')).order_by('d')
        revenue_series = revenue_qs.annotate(d=TruncDate('order__created_at')).values('d').annotate(total=Sum('line_total')).order_by('d')
        return Response({
            'orders': list(orders_series),
            'revenue': list(revenue_series),
        })


class StaffStatsLowStockView(APIView):
    """Liste des produits sous seuil."""
    permission_classes = [permissions.IsAuthenticated, IsStaffRole]

    def get(self, request):
        lows = Inventory.objects.select_related('product').filter(qty_available__lte=Inventory.low_stock_threshold.field.default)
        data = [
            {'product_id': inv.product_id, 'product_name': inv.product.name if inv.product else None, 'qty_available': inv.qty_available, 'low_stock_threshold': inv.low_stock_threshold}
            for inv in lows
        ]
        return Response({'low_stock': data})


class StaffStatsTopProductsView(APIView):
    """Top produits par quantité vendue sur N jours (par défaut 30)."""
    permission_classes = [permissions.IsAuthenticated, IsStaffRole]

    def get(self, request):
        days = int(request.query_params.get('days', '30'))
        since = timezone.now() - timezone.timedelta(days=days)
        paid_like = [Order.Status.PAID, Order.Status.IN_PREPARATION, Order.Status.READY_FOR_PICKUP, Order.Status.PICKED_UP, Order.Status.CLOSED]
        qs = (
            OrderItem.objects.filter(order__status__in=paid_like, order__created_at__gte=since)
            .values('product_id', 'name')
            .annotate(qty=Sum('quantity'), amount=Sum('line_total'))
            .order_by('-qty')[:20]
        )
        return Response({'top': list(qs)})
