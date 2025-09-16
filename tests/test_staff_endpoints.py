from django.test import TestCase, Client
from django.contrib.auth import get_user_model

User = get_user_model()


class StaffEndpointsAuthTests(TestCase):
    def setUp(self):
        self.c = Client()
        self.staff = User.objects.create_user(username='staff1', password='pass123', role='admin')

    def test_users_requires_auth(self):
        r = self.c.get('/api/auth/staff/users')
        assert r.status_code in (401, 403)
        assert 'detail' in r.json()

    def test_inventory_requires_auth(self):
        r = self.c.get('/api/inventory/staff/inventory')
        assert r.status_code in (401, 403)
        assert 'detail' in r.json()
