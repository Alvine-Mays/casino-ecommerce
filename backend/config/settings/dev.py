from .base import *  # noqa
# Local dev: utiliser SQLite si aucune BDD n'est configurée
try:
    from pathlib import Path
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(Path(__file__).resolve().parents[3] / 'db.sqlite3'),
        }
    }
except Exception:
    pass


DEBUG = True
ALLOWED_HOSTS = ['*']
