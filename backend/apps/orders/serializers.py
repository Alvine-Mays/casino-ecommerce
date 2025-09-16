from decimal import Decimal
from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from backend.apps.catalog.models import Product
from backend.apps.inventory.services import reserve_stock, release_stock
from .models import Cart, CartItem, Order, OrderItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['user', 'items', 'updated_at']
        read_only_fields = ['user', 'updated_at']


class AddCartItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        try:
            Product.objects.get(id=attrs['product_id'])
        except Product.DoesNotExist:
            raise serializers.ValidationError('Produit introuvable')
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        cart, _ = Cart.objects.get_or_create(user=user)
        item, created = CartItem.objects.get_or_create(cart=cart, product_id=self.validated_data['product_id'])
        if created:
            item.quantity = self.validated_data['quantity']
        else:
            item.quantity += self.validated_data['quantity']
        item.save()
        return item


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'name', 'unit_price', 'quantity', 'line_total']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'status', 'total_amount', 'currency',
            'contact_name', 'contact_phone', 'contact_email',
            'pickup_date', 'pickup_start', 'pickup_end', 'items',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['status', 'total_amount', 'currency', 'created_at', 'updated_at']


class CreateOrderSerializer(serializers.Serializer):
    contact_name = serializers.CharField(max_length=255)
    contact_phone = serializers.CharField(max_length=64)
    contact_email = serializers.EmailField(required=False, allow_blank=True)
    pickup_date = serializers.DateField()
    pickup_start = serializers.TimeField()
    pickup_end = serializers.TimeField()

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user
        cart = Cart.objects.select_for_update().get(user=user)
        cart_items = list(cart.items.select_related('product'))
        if not cart_items:
            raise serializers.ValidationError('Panier vide')

        # Anti-surréservation
        from django.conf import settings
        date = validated_data['pickup_date']
        start = validated_data['pickup_start']
        end = validated_data['pickup_end']
        capacity = int(getattr(settings, 'PICKUP_SLOTS_DEF', {}).get('capacity', 20))
        active_statuses = [
            Order.Status.CREATED,
            Order.Status.PAID,
            Order.Status.IN_PREPARATION,
            Order.Status.READY_FOR_PICKUP,
        ]
        existing = Order.objects.select_for_update().filter(
            pickup_date=date, pickup_start=start, pickup_end=end, status__in=active_statuses
        ).count()
        if existing >= capacity:
            raise serializers.ValidationError('Créneau complet, veuillez choisir un autre horaire')

        order = Order.objects.create(user=user, **validated_data)
        total = Decimal('0.00')
        reserved = []
        for ci in cart_items:
            product = ci.product
            price = product.current_price()
            unit = price.amount if price else Decimal('0.00')
            line_total = unit * ci.quantity
            ok = reserve_stock(product, ci.quantity)
            if not ok:
                for p, q in reserved:
                    release_stock(p, q)
                raise serializers.ValidationError(f'Stock indisponible pour {product.name}')
            reserved.append((product, ci.quantity))
            OrderItem.objects.create(
                order=order, product=product, name=product.name, unit_price=unit,
                quantity=ci.quantity, line_total=line_total
            )
            total += line_total
        order.total_amount = total
        order.save()
        cart.items.all().delete()
        return order
