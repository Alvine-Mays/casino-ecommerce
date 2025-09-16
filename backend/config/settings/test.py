from .base import *  # noqa

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test.sqlite3',
    }
}
CHANNEL_LAYERS = { 'default': { 'BACKEND': 'channels.layers.InMemoryChannelLayer' } }
CELERY_TASK_ALWAYS_EAGER = True
