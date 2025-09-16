from django.urls import path
from .views import ValidateTempCodeView, SendFinalCodeView, ValidateFinalCodeView

urlpatterns = [
    path('staff/pickup/validate-temp', ValidateTempCodeView.as_view(), name='pickup_validate_temp'),
    path('staff/pickup/send-final', SendFinalCodeView.as_view(), name='pickup_send_final'),
    path('staff/pickup/validate-final', ValidateFinalCodeView.as_view(), name='pickup_validate_final'),
]
