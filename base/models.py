from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal
from uuid import uuid4

# Create your models here.

User = get_user_model()


class Category(models.Model):
    name = models.CharField('category name', max_length=255)
    description = models.TextField('category description', blank=True, null=True)
    code = models.CharField('category code', max_length=255, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='categories/images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Specification(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class SpecificationOption(models.Model):
    value = models.CharField(max_length=255)
    specification = models.ForeignKey(Specification, related_name="specification_option", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.specification.name}/{self.value}"


class Product(models.Model):
    class Meta:
        ordering = ['created_at']

    name = models.CharField('product name', max_length=255)
    description = models.TextField('description', blank=True, null=True)
    code = models.CharField('product code', max_length=255, blank=True, null=True)
    price = models.DecimalField('product price', decimal_places=2, max_digits=10)
    quantity = models.IntegerField('product quantity', default=0)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    is_available = models.BooleanField('product availability', default=True)
    image = models.ImageField(upload_to='products/images/', blank=True, null=True)
    product_specifications = models.ManyToManyField(
        SpecificationOption, through='ProductSpecification', related_name='specifications', blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def rating(self):
        rating = self.product_rating.aggregate(models.Avg("score"))['score__avg']
        return rating

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    class Meta:
        unique_together = ('product', 'specification')

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.ForeignKey(Specification, related_name='specification', on_delete=models.CASCADE)
    option = models.ForeignKey(SpecificationOption, related_name='option', on_delete=models.CASCADE)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField('email', blank=True, null=True, unique=True)
    first_name = models.CharField('first name', max_length=255, blank=True, null=True)
    last_name = models.CharField('last name', max_length=255, blank=True, null=True)
    mobile_number = models.CharField('mobile number', max_length=50, blank=True, null=True)
    address = models.CharField('address', max_length=255, blank=True, null=True)
    post_address = models.CharField('post address', max_length=255, blank=True, null=True)

    def __str__(self):
        return self.email or self.mobile_number

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    class Meta:
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']

    class Status(models.IntegerChoices):
        PEN = 1, "Pending"
        PRO = 2, "Processed"
        DEL = 3, "Delivered"

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    total_price = models.DecimalField(
        'total order price',
        default=0.00,
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    status = models.IntegerField('Order status', choices=Status.choices,  default=Status.PEN)
    uuid = models.CharField(max_length=36, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.uuid}_{self.created_at}"

    def calculate_total_price(self):
        order_items = self.order_items.all()
        for item in order_items:
            price_to_add = item.product.price * item.quantity
            self.total_price = Decimal(self.total_price) + Decimal(price_to_add)
        self.save()

    def set_unique_id(self):
        self.uuid = uuid4()
        self.save()

    def delete(self, *args, **kwargs):
        order_items = self.order_items.all()
        for item in order_items:
            item.product.quantity += item.quantity
            item.product.save()
        super(Order, self).delete(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('product quantity', default=1, null=True, blank=True)

    def __str__(self):
        return f"{self.order.id}: {self.product.name}_{self.quantity}"

    def save(self, *args, **kwargs):
        self.product.quantity -= self.quantity
        self.product.save()
        super(OrderItem, self).save(*args, **kwargs)


class ProductRating(models.Model):
    class Meta:
        unique_together = ('user', 'product',)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="product_rating", on_delete=models.CASCADE)
    score = models.IntegerField(null=True, blank=True, validators=(MinValueValidator(1), MaxValueValidator(5),))


class City(models.Model):
    class Meta:
        verbose_name_plural = "cities"

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"


class NPDepartment(models.Model):
    department = models.CharField(max_length=200)
    address = models.TextField()
    city = models.ForeignKey(City, related_name="department_city", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.department}/{self.city} {self.address}"

# @receiver(post_delete, sender=Order)
# def update_product_quantity(sender, instance, **kwargs):
#     products = instance.order_items.all()
#     instance.product.quantity -= instance.quantity
#     instance.order.total_price += total
