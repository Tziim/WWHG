from django.contrib import admin
from .models import Product, Category, UserProfile, ShoppingCart, CartItem
from .models import SiteConfiguration

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


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ('site', 'num_random_products')
