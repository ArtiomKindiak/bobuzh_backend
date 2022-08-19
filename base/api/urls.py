from django.urls import path
from . import views
from .views import (MyTokenObtainPairView, RegisterView,
                    CategoryListCreateView, CategoryRetrieveUpdateDeleteView,
                    ProductListCreateView, ProductRetrieveUpdateDeleteView)

from rest_framework_simplejwt.views import (
    TokenRefreshView
)

urlpatterns = [
    path('', views.get_routes),

    path('auth/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('store/categories/', CategoryListCreateView.as_view(), name='categories'),
    path('store/categories/<int:pk>/', CategoryRetrieveUpdateDeleteView.as_view(), name='categories/id'),
    path('store/products/', ProductListCreateView.as_view(), name='products'),
    path('store/products/<int:pk>', ProductRetrieveUpdateDeleteView, name='products/id')
]
