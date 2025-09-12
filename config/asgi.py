import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.config.settings.dev')
django.setup()

from backend.apps.orders.consumers import StaffOrdersConsumer  # noqa: E402

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter([
        path('ws/staff/orders/', StaffOrdersConsumer.as_asgi()),
    ]),
})
