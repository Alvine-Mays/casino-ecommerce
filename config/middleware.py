import uuid
from typing import Callable
from django.utils.deprecation import MiddlewareMixin


class RequestIdMiddleware(MiddlewareMixin):
    def process_request(self, request):
        rid = request.headers.get('X-Request-ID') or str(uuid.uuid4())
        request.request_id = rid

    def process_response(self, request, response):
        rid = getattr(request, 'request_id', str(uuid.uuid4()))
        response['X-Request-ID'] = rid
        return response
