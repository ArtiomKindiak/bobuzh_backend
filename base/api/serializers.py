from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from base.models import (
    Category,
    Product,
    Customer,
    Order,
    OrderItem
)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username

        return token


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    if settings.DEBUG:
        password = serializers.CharField(write_only=True, required=True)
    else:
        password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'customer', 'total_price', 'created_at', 'products')

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)

        return order


class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'order', 'quantity',)


class AddOrderItemSerializer(serializers.ModelSerializer):
    # order_id = serializers.IntegerField()

    class Meta:
        model = OrderItem
        fields = ("quantity", "product_id",)

    # def create(self, validated_data, **kwargs):
    #     product = get_object_or_404(Product, id=validated_data['product_id'])
    #
    #     if product.quantity == 0 or not product.is_available:
    #         raise serializers.ValidationError(
    #             {"not available": "the product is not available."}
    #         )
    #
    #     order_item = OrderItem.objects.create(
    #         product=product,
    #         order=kwargs['order'],
    #         quantity=validated_data["quantity"]
    #     )
    #
    #     order_item.save()
    #
    #     product.quantity = product.quantity - order_item.quantity
    #     product.save()
    #
    #     return order_item
