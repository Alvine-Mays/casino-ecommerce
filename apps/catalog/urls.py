from django.urls import path
from .views import (
    CategoryListView,
    ProductListView,
    ProductDetailView,
    FavoriteCreateDeleteView,
    ReviewListCreateView,
)

urlpatterns = [
    path('categories', CategoryListView.as_view(), name='categories_list'),
    path('products', ProductListView.as_view(), name='products_list'),
    path('products/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('favorites', FavoriteCreateDeleteView.as_view(), name='favorite_add_remove'),
    path('reviews', ReviewListCreateView.as_view(), name='reviews_list_create'),
]
