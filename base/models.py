from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

User = get_user_model()


class Category(models.Model):
    name = models.CharField('category name', max_length=255)
    description = models.TextField('category description')
    code = models.CharField('category code', max_length=255, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('product name', max_length=255)
    description = models.TextField('description', blank=True, null=True)
    code = models.CharField('product code', max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField('product price', decimal_places=2, max_digits=10)
    quantity = models.IntegerField('product quantity', default=0)
    brand = models.CharField('product brand', max_length=255)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    is_available = models.BooleanField('product availability', default=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField('email', blank=True, null=True)
    first_name = models.CharField('first name', max_length=255, blank=True, null=True)
    last_name = models.CharField('last name', max_length=255, blank=True, null=True)
    mobile_number = models.CharField('mobile number', max_length=50, blank=True, null=True)
    address = models.CharField('address', max_length=255, blank=True, null=True)
    post_address = models.CharField('post address', max_length=255, blank=True, null=True)


class Order(models.Model):
    class Status(models.TextChoices):
        PEN = "1", "Pending"
        PRO = "2", "Processed"
        DEL = "3", "Delivered"
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    total_price = models.DecimalField(
        'total order price',
        default=0.00,
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    status = models.CharField('Order status', max_length=10, choices=Status.choices,  default=Status.PEN)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.id}_{self.created_at}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('product quantity', default=1)


@receiver(post_save, sender=OrderItem)
def update_order(sender, instance, **kwargs):
    total = instance.quantity * instance.product.price
    instance.product.quantity -= instance.quantity
    instance.order.total_price += total
