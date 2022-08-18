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
        'api/register',
        'api/token',
        'api/token/refresh',
        'api/store/categories'
    ]
    return Response(routes)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def categories_list(request):
    if request.query_params:
        categories = Category.objects.filter(**request.query_params.dict())
    else:
        categories = Category.objects.all()

    print(categories)

    if categories:
        data = CategorySerializer(categories, many=True)
        return Response(data.data)
    else:
        return Response(status=HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_category(request):
    category = CategorySerializer(data=request.data)

    if Category.objects.filter(**request.data).exists():
        raise ValidationError('This data already exists')

    if category.is_valid():
        category.save()
        return Response(category.data)
    else:
        return Response(status=HTTP_404_NOT_FOUND)
