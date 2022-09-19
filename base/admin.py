from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Customer, ProductRating


class OrderItemAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        total = obj.quantity * obj.product.price
        obj.product.quantity -= obj.quantity
        obj.order.total_price += total
        obj.order.save()
        super().save_model(request, obj, form, change)


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ProductRating)
