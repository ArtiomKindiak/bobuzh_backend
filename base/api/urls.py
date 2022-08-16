from django.urls import path
from . import views
from .views import MyTokenObtainPairView, RegisterView, CategoryView

from rest_framework_simplejwt.views import (
    TokenRefreshView
)


urlpatterns = [
    path('', views.getRoutes),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('store/categories', CategoryView.as_view(), name='categories')
]
