from rest_framework import status, permissions, generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .serializers import RegisterSerializer, UserSerializer
from .models import User
from .permissions import IsStaffRole


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class StaffUsersListView(generics.ListAPIView):
    """Liste paginée des utilisateurs pour le staff (recherche par username/email/phone, filtre par role)."""
    serializer_class = UserSerializer
    permission_classes = [IsStaffRole]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'phone', 'first_name', 'last_name']
    ordering = ['-id']
    filterset_fields = ['role']

    def get_queryset(self):
        qs = User.objects.all().order_by('-id')
        q = self.request.query_params.get('q')
        if q:
            qs = qs.filter(
                Q(username__icontains=q) |
                Q(email__icontains=q) |
                Q(phone__icontains=q) |
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q)
            )
        return qs
