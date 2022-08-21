from django.http import JsonResponse

from django.contrib.auth.models import User
from base.models import Category, Product
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import (MyTokenObtainPairSerializer, RegisterSerializer, CategorySerializer, ProductSerializer)
from rest_framework import generics

from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.serializers import ValidationError


@api_view(['GET'])
def get_routes(request):
    routes = [
        'api/auth/register',
        'api/auth/login',
        'api/auth/token/refresh',
        'api/store/categories',
        'api/store/categories/<id>'
    ]
    return Response(routes)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Category.objects.all()
        if params := self.request.query_params:
            params = params.dict()
            queryset = queryset.filter(**params)
        return queryset


class CategoryRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)


class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Product.objects.all()
        if params := self.request.query_params:
            params = params.dict()
            queryset = queryset.filter(**params)
        return queryset


class ProductRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)
