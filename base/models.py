from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField('category name', max_length=255)
    description = models.TextField('category description')
    code = models.CharField('category code', max_length=255, blank=True, null=True)
    parent_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('product name', max_length=255)
    description = models.TextField('description')
    code = models.CharField('product code', max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField('product price', decimal_places=2, max_digits=10)
    quantity = models.IntegerField('product quantity', default=0)
    brand = models.CharField('product brand', max_length=255)
    category_id = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    is_available = models.BooleanField('product availability', default=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.name
