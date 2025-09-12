import os
import json
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
DEBUG = os.getenv('DEBUG', '1') == '1'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
CSRF_TRUSTED_ORIGINS = [o for o in os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',') if o]

LANGUAGE_CODE = 'fr'
TIME_ZONE = os.getenv('TIME_ZONE', 'Africa/Brazzaville')
USE_I18N = True
USE_TZ = True

CURRENCY = 'XAF'
VAT_PERCENT = float(os.getenv('VAT_PERCENT', '18'))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_filters',
    'channels',

    'backend.apps.accounts',
    'backend.apps.catalog',
    'backend.apps.inventory',
    'backend.apps.orders',
    'backend.apps.payments',
    'backend.apps.pickup',
    'backend.apps.notifications',
    'backend.apps.search',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'backend.config.middleware.RequestIdMiddleware',
]

ROOT_URLCONF = 'backend.config.urls'
ASGI_APPLICATION = 'backend.config.asgi.application'
WSGI_APPLICATION = 'backend.config.wsgi.application'


STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': os.getenv('THROTTLE_RATE_ANON', '100/min'),
        'user': os.getenv('THROTTLE_RATE_USER', '1000/min'),
    },
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.getenv('JWT_ACCESS_MINUTES', '30'))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.getenv('JWT_REFRESH_DAYS', '7'))),
    'SIGNING_KEY': os.getenv('JWT_SIGNING_KEY', SECRET_KEY),
    'ALGORITHM': 'HS256',
}

CORS_ALLOW_ALL_ORIGINS = os.getenv('CORS_ALLOW_ALL', '1') == '1'
CORS_ALLOWED_ORIGINS = [o for o in os.getenv('CORS_ALLOWED_ORIGINS', '').split(',') if o]

DATABASES = {}
if os.getenv('DB_URL'):
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
else:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'casino_dev'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'root'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }

REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [REDIS_URL],
        },
    },
}

# Celery
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_TIMEZONE = TIME_ZONE
CELERY_BEAT_SCHEDULE = {
    'ready-reminders-hourly': {
        'task': 'backend.apps.notifications.tasks.schedule_ready_reminders',
        'schedule': 60 * 60,  # hourly
    },
    'auto-cancel-daily': {
        'task': 'backend.apps.notifications.tasks.auto_cancel_not_collected',
        'schedule': 60 * 60 * 6,  # every 6 hours
    },
}

# Pickup slot config
PICKUP_SLOTS_DEF = json.loads(os.getenv('PICKUP_SLOTS_DEF', '{"days":"Mon-Sun","start":"09:00","end":"20:00","slot_minutes":120,"capacity":20}'))
POLICY_EXPIRE_PERISHABLE_HOURS = int(os.getenv('POLICY_EXPIRE_PERISHABLE_HOURS', '24'))
POLICY_EXPIRE_NONPERISHABLE_HOURS = int(os.getenv('POLICY_EXPIRE_NONPERISHABLE_HOURS', '48'))

# Providers
CINETPAY_API_KEY = os.getenv('PAYMENT_CINETPAY_API_KEY', '')
CINETPAY_API_SECRET = os.getenv('PAYMENT_CINETPAY_API_SECRET', '')
CINETPAY_BASE_URL = os.getenv('PAYMENT_CINETPAY_BASE_URL', 'https://api-checkout.cinetpay.com')
AFRICASTALKING_API_KEY = os.getenv('AFRICASTALKING_API_KEY', '')
AFRICASTALKING_SENDER = os.getenv('AFRICASTALKING_SENDER', '')
BREVO_API_KEY = os.getenv('BREVO_API_KEY', '')
BREVO_SENDER = os.getenv('BREVO_SENDER', '')

SITE_BASE_URLS = json.loads(os.getenv('SITE_BASE_URLS', '{"client":"http://localhost:5173","staff":"http://localhost:5174"}'))

# Logging JSON + request-id
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'fmt': '%(asctime)s %(levelname)s %(name)s %(message)s %(request_id)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # tu peux créer un dossier templates/ si besoin
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
