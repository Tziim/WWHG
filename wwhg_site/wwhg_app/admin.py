from django.contrib import admin
from .models import Product, Category, UserProfile, ShoppingCart, CartItem
from .models import SiteConfiguration, ContactInfo, Order, OrderItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


class ShoppingCartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
    'user', 'first_name', 'last_name', 'email', 'phone_number', 'home_address',
    'city', 'country', 'postcode')
    # Add other fields you want to display in the list view

    # Fields to exclude from the detail view and form in admin panel
    exclude = ('card_name', 'card_number', 'exp_month', 'exp_year', 'cvv')

    # Override the method to disable editing
    def has_change_permission(self, request, obj=None):
        return False


class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'phone_number', 'question')
    # Add other fields you want to display in the list view

    # Fields to include in the detail view and form in admin panel
    fields = ('first_name', 'email', 'phone_number', 'question')

    # Override the method to disable editing
    def has_change_permission(self, request, obj=None):
        return False


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_date', 'total_price')
    list_filter = ('order_date',)
    inlines = [OrderItemInline]


# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(ContactInfo, ContactInfoAdmin)
admin.site.register(Order, OrderAdmin)


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ('site', 'num_random_products')
