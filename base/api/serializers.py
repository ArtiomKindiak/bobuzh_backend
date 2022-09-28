from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from base.models import (
    Category,
    Product,
    Customer,
    Order,
    OrderItem,
    ProductRating,
    ProductSpecification,
    Specification,
    SpecificationOption
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


class SpecificationSerializer(serializers.ModelSerializer):
    specification = serializers.ReadOnlyField(source='specification.name')

    class Meta:
        model = SpecificationOption
        fields = ('specification', 'value')


class ProductSpecificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductSpecification
        fields = ('option',)
        read_only_fields = ('option',)


class ProductSerializer(serializers.ModelSerializer):
    rating = serializers.ReadOnlyField()
    specifications = SpecificationSerializer(many=True, read_only=True, source='product_specifications')

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'code', 'price',
                  'quantity', 'category', 'rating', 'image', 'specifications',)
        read_only_fields = ('created_at', 'updated_at', 'rating', 'image',)


class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = ('user', 'product', 'score',)
        read_only_fields = ('user', 'product',)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'image',)


class CustomerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = Customer
        fields = '__all__'

    def get_or_create(self):
        defaults = self.validated_data.copy()
        identifier = defaults.pop('email')
        return Customer.objects.get_or_create(email=identifier, defaults=defaults)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'product', 'quantity',)

    def validate(self, attrs):
        input_quantity = attrs.get('quantity')
        product = Product.objects.get(pk=attrs['product'].id)
        if not product.is_available or input_quantity > product.quantity:
            raise serializers.ValidationError(
                {"product not available error":
                    {"message": f"Product {product.name} is not available.",
                     "product_id": product.id,
                     "is_available": product.is_available,
                     "available_quantity": product.quantity}
                 }
            )
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ('id', 'customer', 'total_price', 'created_at', 'products', 'uuid', 'order_items')
        read_only_fields = ('id', 'uuid', 'order_items')
        depth = 2
