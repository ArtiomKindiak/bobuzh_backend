from django.urls import path, include
from . import views
from .views import (
    MyTokenObtainPairView, RegisterView, LogoutView, LogoutAllView,
    CategoryViewSet, ProductViewSet, OrderViewSet, FiltersListView,
    CityViewSet, NPDepartmentViewSet,
)

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenRefreshView
)


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'cities', CityViewSet, basename="city")
router.register(r'np_departments', NPDepartmentViewSet, basename="department")

urlpatterns = [
    path('', views.get_routes),

    path('auth/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/logout', LogoutView.as_view(), name='logout'),
    path('auth/logout-all', LogoutAllView.as_view(), name='logout-all'),
    path('store/filters/', FiltersListView.as_view(), name='filters'),
    path('store/', include(router.urls)),
]
