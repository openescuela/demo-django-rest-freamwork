# cars/views.py
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Car, User
from .serializers import CarSerializer, UserSerializer, RegisterSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .filters import CarFilter
# users/views.py
from rest_framework.decorators import api_view, permission_classes


# Custom permission: only sellers can create/edit; others read-only unless owner
class IsSellerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # safe methods allowed to anyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # write operations require authenticated seller
        return request.user and request.user.is_authenticated and request.user.is_seller

    def has_object_permission(self, request, view, obj):
        # read-only allowed
        if request.method in permissions.SAFE_METHODS:
            return True
        # owners (seller) can edit their cars
        return obj.seller == request.user

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'make': ['exact', 'icontains'],
        'year': ['exact', 'gte', 'lte'],
        'is_available': ['exact'],
    }
    search_fields = ['make', 'model', 'description']
    ordering_fields = ['price', 'year', 'created_at']
    ordering = ['-created_at']
    filterset_class = CarFilter

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class RegisterViewSet(viewsets.GenericViewSet):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @action(methods=['post'], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
