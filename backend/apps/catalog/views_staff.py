import csv
import io
import json
import os
import time
from decimal import Decimal
from django.db import transaction
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from backend.apps.accounts.permissions import IsStaffRole
from .models import Category, Product, Price, ProductImage
from .serializers import CategorySerializer, ProductSerializer


class StaffCategoryCreateView(APIView):
    """Création de catégorie (staff). Body: {name, parent_id?, image_url?}
    image_url optionnel: si non fourni, une image par défaut peut être utilisée côté front.
    """
    permission_classes = [IsStaffRole]

    def post(self, request):
        name = (request.data.get('name') or '').strip()
        parent_id = request.data.get('parent_id')
        image_url = request.data.get('image_url') or ''
        if not name:
            return Response({'detail': 'name requis'}, status=400)
        parent = Category.objects.filter(id=parent_id).first() if parent_id else None
        cat = Category.objects.create(name=name, parent=parent)
        if image_url:
            try:
                cat.image_url = image_url
                cat.save(update_fields=['image_url'])
            except Exception:
                pass
        return Response(CategorySerializer(cat).data, status=201)


class StaffProductCreateView(APIView):
    """Création de produit (staff). Body: {name, category_id?, description?, price?}
    Crée le prix courant si fourni.
    """
    permission_classes = [IsStaffRole]

    @transaction.atomic
    def post(self, request):
        name = (request.data.get('name') or '').strip()
        if not name:
            return Response({'detail': 'name requis'}, status=400)
        category_id = request.data.get('category_id')
        description = request.data.get('description') or ''
        price = request.data.get('price')
        category = Category.objects.filter(id=category_id).first() if category_id else None
        p = Product.objects.create(name=name, category=category, description=description, is_active=True)
        if price is not None and str(price) != '':
            Price.objects.create(product=p, amount=Decimal(str(price)), is_current=True)
        return Response(ProductSerializer(p).data, status=201)


class StaffProductsImportView(APIView):
    """Import de produits/prix depuis un fichier CSV/JSON (multipart "file") ou JSON direct ({items:[...]})
    CSV attendu: colonnes name, category, price (optionnelles selon vos fichiers)
    JSON attendu: {items:[{name, category, price}]}
    """
    permission_classes = [IsStaffRole]

    @transaction.atomic
    def post(self, request):
        items = []
        if 'file' in request.FILES:
            f = request.FILES['file']
            filename = f.name.lower()
            data = f.read()
            if filename.endswith('.csv'):
                text = data.decode('utf-8', errors='ignore')
                for row in csv.DictReader(io.StringIO(text)):
                    items.append({
                        'name': row.get('name') or row.get('Product Name') or row.get('product') or '',
                        'category': row.get('category') or row.get('Category') or '',
                        'price': row.get('price') or row.get('Price') or '',
                    })
            elif filename.endswith('.json'):
                try:
                    payload = json.loads(data.decode('utf-8'))
                    items = payload.get('items') or payload
                except Exception:
                    return Response({'detail': 'JSON invalide'}, status=400)
            elif filename.endswith('.xlsx'):
                try:
                    import pandas as pd
                    buf = io.BytesIO(data)
                    df = pd.read_excel(buf)
                    for _, row in df.iterrows():
                        items.append({
                            'name': str(row.get('name') or row.get('Product Name') or row.get('product') or ''),
                            'category': str(row.get('category') or row.get('Category') or ''),
                            'price': row.get('price') or row.get('Price') or '',
                        })
                except Exception:
                    return Response({'detail': 'Lecture Excel échouée (openpyxl requis?)'}, status=400)
            else:
                return Response({'detail': 'Extension non supportée'}, status=400)
        else:
            try:
                payload = request.data if isinstance(request.data, dict) else json.loads(request.body.decode('utf-8'))
                items = payload.get('items') or []
            except Exception:
                return Response({'detail': 'Payload invalide'}, status=400)
        created = 0
        for it in items:
            name = (str(it.get('name') or '')).strip()
            if not name:
                continue
            cat_name = (str(it.get('category') or 'Autres')).strip()
            price = it.get('price')
            cat, _ = Category.objects.get_or_create(name=cat_name)
            p, _ = Product.objects.get_or_create(name=name, defaults={'category': cat, 'is_active': True})
            if price not in [None, '']:
                Price.objects.create(product=p, amount=Decimal(str(price)), is_current=True)
            created += 1
        return Response({'created': created}, status=201)


class StaffCategoryImageUploadView(APIView):
    """Upload image de catégorie. POST multipart: file field "image".
    Enregistre le fichier sous MEDIA/categories/<id>/<timestamp>.<ext> et met à jour image_url.
    """
    permission_classes = [IsStaffRole]

    def post(self, request, category_id: int):
        cat = Category.objects.filter(id=category_id).first()
        if not cat:
            return Response({'detail': 'Catégorie introuvable'}, status=404)
        f = request.FILES.get('image')
        if not f:
            return Response({'detail': 'Champ image manquant'}, status=400)
        name, ext = os.path.splitext(f.name)
        ts = int(time.time())
        rel_path = f"categories/{category_id}/{ts}{ext or '.jpg'}"
        saved_path = default_storage.save(rel_path, ContentFile(f.read()))
        url = request.build_absolute_uri(settings.MEDIA_URL + saved_path)
        cat.image_url = url
        cat.save(update_fields=['image_url'])
        return Response(CategorySerializer(cat).data, status=200)


class StaffProductImageUploadView(APIView):
    """Upload image de produit. POST multipart: file field "image".
    Crée un ProductImage avec image_url pointant vers MEDIA.
    """
    permission_classes = [IsStaffRole]

    def post(self, request, product_id: int):
        prod = Product.objects.filter(id=product_id).first()
        if not prod:
            return Response({'detail': 'Produit introuvable'}, status=404)
        f = request.FILES.get('image')
        if not f:
            return Response({'detail': 'Champ image manquant'}, status=400)
        name, ext = os.path.splitext(f.name)
        ts = int(time.time())
        rel_path = f"products/{product_id}/{ts}{ext or '.jpg'}"
        saved_path = default_storage.save(rel_path, ContentFile(f.read()))
        url = request.build_absolute_uri(settings.MEDIA_URL + saved_path)
        ProductImage.objects.create(product=prod, image_url=url)
        return Response({'product_id': prod.id, 'image_url': url}, status=201)
