from django.db import connection
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from backend.apps.catalog.models import Product


class SuggestView(APIView):
    def get(self, request):
        q = request.query_params.get('q', '').strip()
        results = []
        if q:
            vendor = connection.vendor
            if vendor == 'mysql':
                try:
                    with connection.cursor() as cur:
                        cur.execute(
                            "SELECT id, name FROM catalog_product WHERE MATCH(name, description) AGAINST (%s IN BOOLEAN MODE) LIMIT 10",
                            [q + '*']
                        )
                        rows = cur.fetchall()
                        results = [{ 'id': r[0], 'name': r[1] } for r in rows]
                except Exception:
                    qs = Product.objects.filter(Q(name__icontains=q) | Q(description__icontains=q), is_active=True).values('id', 'name')[:10]
                    results = list(qs)
            else:
                qs = Product.objects.filter(Q(name__icontains=q) | Q(description__icontains=q), is_active=True).values('id', 'name')[:10]
                results = list(qs)
        return Response({'q': q, 'results': results})
