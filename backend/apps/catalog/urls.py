from django.urls import path
from .views import (
    CategoryListView,
    ProductListView,
    ProductDetailView,
    FavoriteCreateDeleteView,
    ReviewListCreateView,
)
from .views_staff import (
    StaffCategoryCreateView,
    StaffProductCreateView,
    StaffProductsImportView,
    StaffCategoryImageUploadView,
    StaffProductImageUploadView,
)

urlpatterns = [
    path('categories', CategoryListView.as_view(), name='categories_list'),
    path('products', ProductListView.as_view(), name='products_list'),
    path('products/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('favorites', FavoriteCreateDeleteView.as_view(), name='favorite_add_remove'),
    path('reviews', ReviewListCreateView.as_view(), name='reviews_list_create'),

    # Staff endpoints (protégés par IsStaffRole)
    path('staff/categories', StaffCategoryCreateView.as_view(), name='staff_category_create'),
    path('staff/products', StaffProductCreateView.as_view(), name='staff_product_create'),
    path('staff/import', StaffProductsImportView.as_view(), name='staff_products_import'),
    path('staff/upload-category/<int:category_id>', StaffCategoryImageUploadView.as_view(), name='staff_category_upload'),
    path('staff/upload-product/<int:product_id>', StaffProductImageUploadView.as_view(), name='staff_product_upload'),
]
