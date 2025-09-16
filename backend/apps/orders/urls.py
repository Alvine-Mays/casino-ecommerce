from django.urls import path
from .views import (
    CartView, CartItemsView, CartItemDetailView,
    CreateOrderView, MyOrdersView, OrderDetailView, SlotsView
)
from .staff_views import (
    StaffOrdersListView, StaffOrderPrepareView, StaffOrderReadyView, StaffOrderHandoverView,
    StaffStatsOverviewView, StaffStatsDailyView, StaffStatsLowStockView, StaffStatsTopProductsView,
)
from backend.apps.pickup.views import ValidateTempCodeView, SendFinalCodeView, ValidateFinalCodeView
from backend.apps.pickup.models import WithdrawalCode
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class OrderCodesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id: int):
        order = get_object_or_404(request.user.orders, id=order_id)
        codes = order.withdrawal_codes.values('kind', 'code', 'expires_at', 'used_at')
        return Response({'order_id': order.id, 'codes': list(codes)})


urlpatterns = [
    path('cart', CartView.as_view(), name='cart_get_put'),
    path('cart/items', CartItemsView.as_view(), name='cart_items_add'),
    path('cart/items/<int:pk>', CartItemDetailView.as_view(), name='cart_item_detail'),
    path('', CreateOrderView.as_view(), name='orders_create'),
    path('mine', MyOrdersView.as_view(), name='orders_mine'),
    path('<int:pk>', OrderDetailView.as_view(), name='orders_detail'),
    path('slots', SlotsView.as_view(), name='orders_slots'),

    # Codes
    path('<int:order_id>/codes', OrderCodesView.as_view(), name='orders_codes'),

    # Staff
    path('staff/orders', StaffOrdersListView.as_view(), name='staff_orders'),
    path('staff/orders/<int:order_id>/prepare', StaffOrderPrepareView.as_view(), name='staff_order_prepare'),
    path('staff/orders/<int:order_id>/ready', StaffOrderReadyView.as_view(), name='staff_order_ready'),
    path('staff/orders/<int:order_id>/handover', StaffOrderHandoverView.as_view(), name='staff_order_handover'),

    # Staff analytics
    path('staff/stats/overview', StaffStatsOverviewView.as_view(), name='staff_stats_overview'),
    path('staff/stats/daily', StaffStatsDailyView.as_view(), name='staff_stats_daily'),
    path('staff/stats/low-stock', StaffStatsLowStockView.as_view(), name='staff_stats_low_stock'),
    path('staff/stats/top-products', StaffStatsTopProductsView.as_view(), name='staff_stats_top_products'),
]
