from django.contrib import admin
from .models import Category, Products, Cart, CartItems, Order, OrderItem, Coupon

# Register your models here.
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(Order)
admin.site.register(OrderItem)

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "discount_type",
        "value",
        "minimum_purchase",
        "valid_from",
        "valid_until",
        "usage_limit",
        "used_count",
        "is_active",
    )

    search_fields = (
        "code",
    )

    list_filter = (
        "discount_type",
        "is_active",
    )