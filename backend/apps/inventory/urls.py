from django.urls import path
from .views import StaffInventoryAdjustView, StaffInventoryListView

urlpatterns = [
    path('staff/inventory', StaffInventoryListView.as_view(), name='staff_inventory_list'),
    path('staff/inventory/<int:product_id>', StaffInventoryAdjustView.as_view(), name='staff_inventory_adjust'),
]
