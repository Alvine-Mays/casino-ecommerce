from rest_framework import serializers
from .models import Category, Product, Price, ProductImage, Favorite, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent']


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['amount', 'currency', 'valid_from', 'is_current']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image_url']


class ProductSerializer(serializers.ModelSerializer):
    current_price = PriceSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'is_active', 'category', 'current_price', 'images']


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'user_name', 'product', 'rating', 'comment', 'is_moderated', 'created_at']
        read_only_fields = ['user', 'is_moderated']


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'product', 'created_at']
        read_only_fields = ['user', 'created_at']
