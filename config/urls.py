from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/', include('backend.apps.accounts.urls')),
    path('api/catalog/', include('backend.apps.catalog.urls')),
    path('api/inventory/', include('backend.apps.inventory.urls')),
    path('api/orders/', include('backend.apps.orders.urls')),
    path('api/payments/', include('backend.apps.payments.urls')),
    path('api/pickup/', include('backend.apps.pickup.urls')),
    path('api/notifications/', include('backend.apps.notifications.urls')),
    path('api/search/', include('backend.apps.search.urls')),
]
