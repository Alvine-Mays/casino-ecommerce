from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from backend.apps.orders.models import Order, OrderItem
from backend.apps.catalog.models import Category, Product, Price
from backend.apps.payments.services import create_intent

User = get_user_model()


class PaymentsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u1', password='p')
        cat = Category.objects.create(name='Autres')
        self.product = Product.objects.create(name='Test', category=cat, is_active=True)
        Price.objects.create(product=self.product, amount=1000, is_current=True)
        self.order = Order.objects.create(
            user=self.user,
            status=Order.Status.CREATED,
            total_amount=1000,
            currency='XAF',
            contact_name='Client Test',
            contact_phone='060000000',
            pickup_date=timezone.now().date(),
            pickup_start=timezone.now().time().replace(microsecond=0),
            pickup_end=timezone.now().time().replace(microsecond=0),
        )
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            name='Test',
            unit_price=1000,
            quantity=1,
            line_total=1000,
        )

    def test_create_intent_default(self):
        data = create_intent(self.order)
        assert 'reference' in data

    def test_create_intent_mtn(self):
        data = create_intent(self.order, provider='mtn_momo')
        assert 'reference' in data
