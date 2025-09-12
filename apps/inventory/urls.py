from django.urls import path
from .views import StaffInventoryAdjustView

urlpatterns = [
    path('staff/inventory/<int:product_id>', StaffInventoryAdjustView.as_view(), name='staff_inventory_adjust'),
]
