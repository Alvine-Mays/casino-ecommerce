from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, Favorite, Review
from .serializers import CategorySerializer, ProductSerializer, FavoriteSerializer, ReviewSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all().select_related('category')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'description']


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all().select_related('category')
    serializer_class = ProductSerializer


class FavoriteCreateDeleteView(generics.GenericAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = FavoriteSerializer(data={**request.data, 'user': request.user.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        user = request.user
        product_id = request.data.get('product')
        Favorite.objects.filter(user=user, product_id=product_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        product_id = self.request.query_params.get('product')
        qs = Review.objects.all().order_by('-created_at')
        if product_id:
            qs = qs.filter(product_id=product_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, is_moderated=False)
