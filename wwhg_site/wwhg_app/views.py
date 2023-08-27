from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, CartItemUpdateForm
from .models import Product, Category, ShoppingCart, CartItem
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .models import UserProfile
from .forms import UserProfileEditForm
from django.contrib.auth.mixins import LoginRequiredMixin
import pyjokes


# Create your views here.
def index(request):
    categories = Category.objects.all()
    user = request.user
    shopping_cart = None
    cart_items = None

    if user.is_authenticated:
        shopping_cart, created = ShoppingCart.objects.get_or_create(user=user)
        cart_items = CartItem.objects.filter(cart=shopping_cart)

    context = {
        'categories': categories,
        'cart_items': cart_items,
        'shopping_cart': shopping_cart,
    }
    return render(request, 'wwhg_app/index.html', context)


def all_products(request, category_id=None):
    products = Product.objects.all()
    user = request.user
    shopping_cart = None
    cart_items = None
    random_joke = pyjokes.get_joke()

    if user.is_authenticated:
        shopping_cart, created = ShoppingCart.objects.get_or_create(user=user)
        cart_items = CartItem.objects.filter(cart=shopping_cart)

    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()

    context = {
        'products': products, 'random_joke': random_joke,
        'categories': categories,
        'cart_items': cart_items,
        'shopping_cart': shopping_cart,
    }

    return render(request, 'wwhg_app/shop/all_products.html', context)


def product_detail(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        # Handle the case where the product with the given ID doesn't exist
        return render(request, 'wwhg_app/shop/product_not_found.html')

    # Retrieve all categories for the menu
    categories = Category.objects.all()
    user = request.user
    shopping_cart = None
    cart_items = None

    if user.is_authenticated:
        shopping_cart, created = ShoppingCart.objects.get_or_create(user=user)
        cart_items = CartItem.objects.filter(cart=shopping_cart)

    context = {
        'product': product,
        'categories': categories,
        'cart_items': cart_items,
        'shopping_cart': shopping_cart,
    }

    return render(request, 'wwhg_app/shop/product_detail.html', context)


def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("/login")
        else:
            print(form.errors)

    else:
        form = RegisterForm()
    return render(response, 'registration/register.html', {"form": form})


@login_required
def user_profile_edit_view(request):
    user_profile = request.user.userprofile
    user = request.user
    shopping_cart, created = ShoppingCart.objects.get_or_create(user=user)
    cart_items = CartItem.objects.filter(cart=shopping_cart)

    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, instance=user_profile)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('edit_profile')
    else:
        form = UserProfileEditForm(instance=user_profile)

    context = {
        'form': form,
        'cart_items': cart_items,
        'shopping_cart': shopping_cart,
    }

    return render(request, 'registration/edit_profile.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = request.user
    shopping_cart, created = ShoppingCart.objects.get_or_create(user=user)

    # Retrieve the quantity from the form data
    quantity = int(request.POST.get('quantity', 1))

    # Check if the product is already in the cart
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=shopping_cart, product=product)

    if not item_created:
        # If the item is already in the cart, update the quantity
        cart_item.quantity += quantity
        cart_item.save()
    else:
        cart_item.quantity = quantity
        cart_item.save()

    return redirect('view_cart')


def view_cart(request):
    user = request.user
    shopping_cart, created = ShoppingCart.objects.get_or_create(user=user)
    cart_items = CartItem.objects.filter(cart=shopping_cart)
    categories = Category.objects.all()

    context = {
        'cart_items': cart_items,
        'shopping_cart': shopping_cart,
        'categories': categories,
    }

    return render(request, 'cart/update_cart_item.html', context)


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id)
    cart_item.delete()
    return redirect('view_cart')


@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'increment':
            cart_item.quantity += 1
        elif action == 'decrement' and cart_item.quantity > 1:
            cart_item.quantity -= 1

        cart_item.save()

    return redirect('view_cart')


def checkout(request):
    user = request.user
    shopping_cart, created = ShoppingCart.objects.get_or_create(user=user)
    cart_items = CartItem.objects.filter(cart=shopping_cart)
    categories = Category.objects.all()

    # Retrieve the user's profile
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None

    context = {
        'cart_items': cart_items,
        'shopping_cart': shopping_cart,
        'categories': categories,
        'user_profile': user_profile,
    }
    return render(request, 'cart/checkout.html', context)

