import uuid
import time
import logging
from django.utils.deprecation import MiddlewareMixin


class RequestIdMiddleware(MiddlewareMixin):
    """Assigne un X-Request-ID à chaque requête/réponse pour la corrélation des logs."""
    def process_request(self, request):
        rid = request.headers.get('X-Request-ID') or str(uuid.uuid4())
        request.request_id = rid

    def process_response(self, request, response):
        rid = getattr(request, 'request_id', str(uuid.uuid4()))
        response['X-Request-ID'] = rid
        return response


class RequestLoggingMiddleware(MiddlewareMixin):
    """Log minimal par requête (méthode, chemin, statut, durée, user, ip)."""
    def process_request(self, request):
        request._start_time = time.monotonic()

    def process_response(self, request, response):
        try:
            duration_ms = None
            try:
                duration_ms = round((time.monotonic() - getattr(request, '_start_time', time.monotonic())) * 1000, 2)
            except Exception:
                pass
            logger = logging.getLogger('request')
            user = getattr(request, 'user', None)
            user_id = getattr(user, 'id', None) if user is not None and getattr(user, 'is_authenticated', False) else None
            rid = getattr(request, 'request_id', None)
            logger.info(
                'HTTP %s %s',
                request.method,
                request.get_full_path(),
                extra={
                    'status_code': getattr(response, 'status_code', None),
                    'duration_ms': duration_ms,
                    'request_id': rid,
                    'user_id': user_id,
                    'remote_addr': self._get_ip(request),
                },
            )
        finally:
            return response

    def _get_ip(self, request):
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        if xff:
            return xff.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')
