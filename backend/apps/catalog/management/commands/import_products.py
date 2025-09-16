from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from decimal import Decimal
import os

try:
    import kagglehub
    import pandas as pd
except Exception:  # pragma: no cover
    kagglehub = None
    pd = None

from backend.apps.catalog.models import Category, Product, Price


class Command(BaseCommand):
    help = 'Importe des produits depuis un dataset Kaggle ou un fichier CSV local'

    def add_arguments(self, parser):
        parser.add_argument('--dataset', type=str, help='Ex: anvitkumar/shopping-dataset')
        parser.add_argument('--file', type=str, help='CSV local')
        parser.add_argument('--rate', type=float, default=600.0, help='Taux USD->XAF approx')

    @transaction.atomic
    def handle(self, *args, **options):
        dataset = options.get('dataset')
        file = options.get('file')
        rate = Decimal(str(options.get('rate') or 600.0))

        if file and os.path.exists(file):
            df = pd.read_csv(file)
        elif dataset:
            if not kagglehub:
                raise CommandError('kagglehub/pandas requis')
            path = kagglehub.dataset_download(dataset)
            # naive: cherry pick first csv
            csvs = [f for f in os.listdir(path) if f.endswith('.csv')]
            if not csvs:
                raise CommandError('Aucun CSV trouvé dans le dataset')
            df = pd.read_csv(os.path.join(path, csvs[0]))
        else:
            raise CommandError('Spécifier --dataset ou --file')

        count = 0
        for _, row in df.head(200).iterrows():  # limiter pour démo
            name = str(row.get('Product Name') or row.get('name') or row.get('product') or f"Produit {count}")
            cat_name = str(row.get('Category') or row.get('category') or 'Autres')
            price_usd = Decimal(str(row.get('Price') or row.get('price') or '1.0'))
            price_xaf = (price_usd * rate).quantize(Decimal('1.00'))

            cat, _ = Category.objects.get_or_create(name=cat_name)
            p, created = Product.objects.get_or_create(name=name, defaults={'category': cat, 'is_active': True})
            if created:
                Price.objects.create(product=p, amount=price_xaf, is_current=True)
            count += 1

        self.stdout.write(self.style.SUCCESS(f"Import terminé: {count} produits"))
