from django.contrib import admin
from .models import (
    Category, Product, Order, OrderItem, Customer, Specification, SpecificationOption,
    ProductSpecification
)


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
    list_display = ('id', 'name',)


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemAdmin,)
    list_display = ('uuid', 'customer', 'total_price', 'status', 'created_at')
    fields = ('customer', 'status', 'uuid')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'mobile_number')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'slug', 'created_at')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Specification, SpecificationAdmin)
