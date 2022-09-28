from django.contrib import admin
from .models import (
    Category, Product, Order, OrderItem, Customer, Specification, SpecificationOption,
    ProductSpecification
)


class OrderItemAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        total = obj.quantity * obj.product.price
        obj.product.quantity -= obj.quantity
        obj.order.total_price += total
        obj.order.save()
        super().save_model(request, obj, form, change)


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1


class SpecificationOptionInline(admin.StackedInline):
    model = SpecificationOption
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'price', 'quantity', 'category', 'rating', 'is_available', 'created_at')
    inlines = (ProductSpecificationInline,)


class SpecificationAdmin(admin.ModelAdmin):
    inlines = (SpecificationOptionInline,)


admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Specification, SpecificationAdmin)
