from django.contrib import admin
from .models import Product, Order, Category, UserProfile

# Register your models here.

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(UserProfile)
