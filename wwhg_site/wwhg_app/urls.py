"""
URL configuration for wwhg_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views. home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls')).
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('products/', views.all_products, name='all_products'),
    path('product/<int:product_id>/', views.product_detail,
         name='product_detail'),
    path('products/<int:category_id>/', views.all_products,
         name='all_products'),

    path('add_to_cart/<int:product_id>/', views.add_to_cart,
         name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart,
         name='remove_from_cart'),
    path('clear_cart/', views.remove_all_items_from_cart, name='clear_cart'),
    path('update_cart_item/<int:item_id>/', views.update_cart_item,
         name='update_cart_item'),
    path('cart/update/<int:item_id>/', views.update_cart_item,
         name='update_cart_item'),
    path('checkout/', views.checkout,
         name='checkout'),
    path('payment-confirmation/', views.payment_confirmation, name='payment_confirmation'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
