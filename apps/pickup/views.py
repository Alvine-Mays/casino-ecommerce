from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ValidateCodeSerializer
from .models import WithdrawalCode
from .services import validate_code, generate_final_code
from backend.apps.notifications.tasks import send_final_code


class ValidateTempCodeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ValidateCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        wc = validate_code(WithdrawalCode.Kind.TEMP, code)
        if not wc:
            return Response({'valid': False}, status=status.HTTP_200_OK)
        return Response({'valid': True, 'order_id': wc.order_id})


class SendFinalCodeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ValidateCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        wc = validate_code(WithdrawalCode.Kind.TEMP, code)
        if not wc:
            return Response({'detail': 'Code invalide'}, status=400)
        final = generate_final_code(wc.order)
        send_final_code.delay(wc.order_id, final.code)
        return Response({'sent': True})


class ValidateFinalCodeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ValidateCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        wc = validate_code(WithdrawalCode.Kind.FINAL, code)
        if not wc:
            return Response({'valid': False}, status=200)
        order = wc.order
        if order.status == order.Status.READY_FOR_PICKUP:
            order.status = order.Status.PICKED_UP
            order.save(update_fields=['status'])
        wc.used_at = wc.used_at or wc.expires_at  # mark as used
        wc.save(update_fields=['used_at'])
        return Response({'valid': True, 'order_id': order.id})
