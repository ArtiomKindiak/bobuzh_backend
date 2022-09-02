from django.http import JsonResponse

from django.contrib.auth.models import User
from base.models import Category, Product, Order, OrderItem
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    CategorySerializer,
    ProductSerializer,
    CustomerSerializer,
    OrderSerializer,
    OrderItemSerializer,
    AddOrderItemSerializer,
)
from rest_framework import generics, status, viewsets
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken


@api_view(['GET'])
def get_routes(request):
    routes = [
        'api/auth/register/',
        'api/auth/login/',
        'api/auth/token/refresh/',
        'api/auth/logout/',
        'api/auth/logout-all/',
        'api/store/categories/',
        'api/store/categories/<id>/',
        'api/store/products/',
        'api/store/products/<id>'
    ]
    return Response(routes)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user_id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)


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


class OrderViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Order.objects.all()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        order = Order.objects.create()

        data = request.data['products']
        serializer = AddOrderItemSerializer(data)
        order_item = OrderItem.objects.create(**serializer.data, order_id=order.id)

        order_serializer = OrderSerializer(order)
        return Response(order_serializer.data)
