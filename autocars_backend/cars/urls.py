# cars/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CarViewSet, RegisterViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import me

router = DefaultRouter()
router.register(r'cars', CarViewSet, basename='cars')
router.register(r'auth', RegisterViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("users/me/", me, name="user_me"),
]
