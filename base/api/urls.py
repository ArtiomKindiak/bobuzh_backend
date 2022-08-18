from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views
from .views import MyTokenObtainPairView, RegisterView

from rest_framework_simplejwt.views import (
    TokenRefreshView
)


class OptionalSlashRouter(SimpleRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'


urlpatterns = [
    path('', views.get_routes),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('store/categories/', views.categories_list, name='categories'),
    path('store/categories/create/', views.add_category, name='add_category')
]
