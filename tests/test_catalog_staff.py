from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from backend.apps.catalog.models import Category, Product

User = get_user_model()


class CatalogStaffTests(TestCase):
    def setUp(self):
        self.c = Client()
        self.staff = User.objects.create_user(username='admin1', password='pass123', role='admin')
        self.c.login(username='admin1', password='pass123')

    def test_create_category(self):
        r = self.c.post('/api/catalog/staff/categories', {'name': 'Boissons'})
        assert r.status_code == 201
        assert Category.objects.filter(name='Boissons').exists()

    def test_upload_category_image(self):
        cat = Category.objects.create(name='Fruits')
        img = SimpleUploadedFile('test.jpg', b'fakejpegdata', content_type='image/jpeg')
        r = self.c.post(f'/api/catalog/staff/upload-category/{cat.id}', {'image': img})
        assert r.status_code == 200
        cat.refresh_from_db()
        assert cat.image_url and 'categories/' in cat.image_url

    def test_import_products_json(self):
        payload = {
            'items': [
                {'name': 'Cola 33cl', 'category': 'Boissons', 'price': '500'},
                {'name': 'Jus Orange 1L', 'category': 'Boissons', 'price': '1200'},
            ]
        }
        r = self.c.post('/api/catalog/staff/import', payload, content_type='application/json')
        assert r.status_code == 201
        assert Product.objects.filter(name='Cola 33cl').exists()
        assert Product.objects.filter(name='Jus Orange 1L').exists()
