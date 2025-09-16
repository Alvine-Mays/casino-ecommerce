from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# Endpoint de santé minimal pour vérifier la connectivité depuis le frontend et les scripts
# Retourne {"status":"ok"} si l'application répond correctement
# Utilisé par le test Django et le test d'intégration Vite
def health(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health),
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

# Service des fichiers MEDIA en développement uniquement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
