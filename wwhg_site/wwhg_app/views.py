from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "wwhg_app/index.html", {})


def all_products(request):
    # Fetch all products from the database and pass them to the template
    # Replace this with actual database querying logic
    products = []
    return render(request, 'wwhg_app/shop/all_products.html', {'products': products})


def product_detail(request, product_id):
    # Fetch the specific product from the database based on product_id
    # Replace this with actual database querying logic
    product = None
    return render(request, 'wwhg_app/shop/product_detail.html', {'product': product})
