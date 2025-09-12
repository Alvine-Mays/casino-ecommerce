from datetime import datetime, time, timedelta
from django.conf import settings
from django.utils import timezone
from django.db.models import Count
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, ListAPIView
from .models import Cart, CartItem, Order
from .serializers import (
    CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer,
    CreateOrderSerializer, OrderSerializer
)


class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return Response(CartSerializer(cart).data)

    def put(self, request):
        # Replace the whole cart items with provided list
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = request.data.get('items', [])
        cart.items.all().delete()
        for it in items:
            serializer = CartItemSerializer(data={
                'product': it['product'],
                'quantity': it.get('quantity', 1)
            })
            serializer.is_valid(raise_exception=True)
            serializer.save(cart=cart)
        return Response(CartSerializer(cart).data)


class CartItemsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = AddCartItemSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        item = serializer.save()
        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)


class CartItemDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk: int):
        item = CartItem.objects.get(pk=pk, cart__user=request.user)
        serializer = UpdateCartItemSerializer(item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(CartItemSerializer(item).data)

    def delete(self, request, pk: int):
        CartItem.objects.filter(pk=pk, cart__user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class MyOrdersView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


class OrderDetailView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class SlotsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        date_str = request.query_params.get('date')
        if not date_str:
            return Response({'detail': 'date=YYYY-MM-DD requis'}, status=400)
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        cfg = settings.PICKUP_SLOTS_DEF
        start_h, start_m = map(int, cfg['start'].split(':'))
        end_h, end_m = map(int, cfg['end'].split(':'))
        slot_minutes = int(cfg.get('slot_minutes', 120))
        capacity = int(cfg.get('capacity', 20))

        slots = []
        start_dt = datetime.combine(date, time(start_h, start_m))
        end_dt = datetime.combine(date, time(end_h, end_m))
        cur = start_dt
        while cur < end_dt:
            s = cur
            e = cur + timedelta(minutes=slot_minutes)
            orders_count = Order.objects.filter(pickup_date=date, pickup_start=s.time(), pickup_end=e.time()).count()
            remaining = max(0, capacity - orders_count)
            slots.append({
                'start': s.time().strftime('%H:%M'),
                'end': e.time().strftime('%H:%M'),
                'capacity': capacity,
                'remaining': remaining,
            })
            cur = e
        return Response({'date': date_str, 'slots': slots})
