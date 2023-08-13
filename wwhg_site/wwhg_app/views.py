from django.shortcuts import render
from .models import Product, Category


# Create your views here.
def index(request):
    return render(request, "wwhg_app/index.html", {})


def all_products(request):
    selected_category_id = request.GET.get('category')
    products = Product.objects.all()
    if selected_category_id:
        products = Product.objects.filter(category_id=selected_category_id)

    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
    }

    return render(request, 'wwhg_app/shop/all_products.html', context)


def product_detail(request, product_id):
    # Fetch the specific product from the database based on product_id
    # Replace this with actual database querying logic
    product = None
    return render(request, 'wwhg_app/shop/product_detail.html',
                  {'product': product})
