from django.shortcuts import render
from .models import Product, Category
from django.http import HttpResponse

# Create your views here.
def index(request):
    categories = Category.objects.all()
    # print(categories)  # testimiseks kui categories ei tööta
    context = {'categories': categories}
    return render(request, 'wwhg_app/index.html', context)

# Test versioon töös kui vaja kustutame selle ära.
# def all_products(request):
#     selected_category_id = request.GET.get('category')
#     products = Product.objects.all()
#     if selected_category_id:
#         products = Product.objects.filter(category_id=selected_category_id)
#
#     categories = Category.objects.all()
#
#     context = {
#         'products': products,
#         'categories': categories,
#     }
#
#     return render(request, 'wwhg_app/shop/all_products.html', context)

def all_products(request, category_id=None):
    products = Product.objects.all()

    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
    }

    return render(request, 'wwhg_app/shop/all_products.html', context)


def product_detail(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        # Handle the case where the product with the given ID doesn't exist
        return render(request, 'wwhg_app/shop/product_not_found.html')

    return render(request, 'wwhg_app/shop/product_detail.html', {'product': product})


def category_detail(request, pk):
    # Retrieve the category object using the pk parameter
    category = Category.objects.get(pk=pk)

    # You can add more logic here if needed

    return render(request, 'wwhg_app/index.html', {'category': category})