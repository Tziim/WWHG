from django.contrib import admin
from .models import Product, Category, UserProfile, ShoppingCart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


class ShoppingCartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]


# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
