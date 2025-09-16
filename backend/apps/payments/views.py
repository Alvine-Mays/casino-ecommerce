from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from backend.apps.orders.models import Order
from .services import create_intent, handle_webhook


class CreatePaymentIntentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order_id')
        provider = request.data.get('method') or request.data.get('provider')
        order = get_object_or_404(Order, id=order_id, user=request.user)
        data = create_intent(order, provider)
        return Response(data, status=status.HTTP_201_CREATED)


class PaymentWebhookView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        result = handle_webhook(request.data)
        return Response(result)
