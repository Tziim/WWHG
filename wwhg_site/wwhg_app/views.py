from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sessions.models import Session
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import RegisterForm, CartItemUpdateForm
from .models import Product, Category, ShoppingCart, CartItem
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .models import UserProfile
from .forms import UserProfileEditForm
from django.contrib.auth.mixins import LoginRequiredMixin
import pyjokes
from time import sleep
from django.core.exceptions import ObjectDoesNotExist
import requests
import datetime
import json
from datetime import datetime
from .models import Product
import random


# Create your views here.
def index(request):
    # Fetch random products
    products = Product.objects.all()
    num_products = products.count()
    num_samples = min(16, num_products)  # How many random products in page
    random_products = random.sample(list(products), num_samples)

    categories = Category.objects.all()
    user = request.user
    shopping_cart = None
    cart_items = None

    next_holiday_data = fetch_next_holiday()

    if user.is_authenticated:
        shopping_cart, created = ShoppingCart.objects.get_or_create(user=user)
        cart_items = CartItem.objects.filter(cart=shopping_cart)

    else:
        # For anonymous users, use the session to store cart information
        session_cart_id = request.session.get('session_cart_id', None)

        if session_cart_id is None:
            # Create a new shopping cart for the session
            session_cart = ShoppingCart()
            session_cart.save()
            request.session['session_cart_id'] = session_cart.id
        else:
            # Retrieve the existing shopping cart
            session_cart = ShoppingCart.objects.get(id=session_cart_id)

        shopping_cart = session_cart

    context = {
        'categories': categories,
        'cart_items': cart_items,
        'shopping_cart': shopping_cart,
        'random_products': random_products,  # Pass the random products to the template
    }
    context.update(next_holiday_data)  # merge the next holiday data with the existing context

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
    else:
        session_cart_id = request.session.get('session_cart_id', None)
        if session_cart_id is None:
            # Create a new shopping cart for the session
            session_cart = ShoppingCart()
            session_cart.save()
            request.session['session_cart_id'] = session_cart.id
        else:
            # Retrieve the existing shopping cart
            session_cart = ShoppingCart.objects.get(id=session_cart_id)

        shopping_cart = session_cart

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
    product = get_object_or_404(Product, pk=product_id)

    # Retrieve all categories for the menu
    categories = Category.objects.all()
    user = request.user
    shopping_cart = None
    cart_items = None

    if user.is_authenticated:
        shopping_cart, created = ShoppingCart.objects.get_or_create(user=user)
        cart_items = CartItem.objects.filter(cart=shopping_cart)

    else:
        # For anonymous users, use the session to store cart information
        session_cart_id = request.session.get('session_cart_id', None)

        if session_cart_id is None:
            # Create a new shopping cart for the session
            session_cart = ShoppingCart()
            session_cart.save()
            request.session['session_cart_id'] = session_cart.id
        else:
            # Retrieve the existing shopping cart
            session_cart = ShoppingCart.objects.get(id=session_cart_id)

        shopping_cart = session_cart

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
            messages.success(response, 'Account Successfully Created')
            return redirect("/login")
        else:
            messages.error(response,
                           'Form is not valid, Account have not been created')
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
            messages.success(request, 'Successfully Saved')
            return redirect('edit_profile')
        else:
            messages.error(request,
                           'Form is not valid, changes have not been saved')
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

    if user.is_authenticated:
        # For authenticated users, use the user's cart
        shopping_cart, created = ShoppingCart.objects.get_or_create(user=user)
    else:
        # For anonymous users, use the session to store cart information
        session_cart_id = request.session.get('session_cart_id', None)

        if session_cart_id is None:
            # Create a new shopping cart for the session
            session_cart = ShoppingCart()
            session_cart.save()
            request.session['session_cart_id'] = session_cart.id
        else:
            # Retrieve the existing shopping cart
            session_cart = ShoppingCart.objects.get(id=session_cart_id)

        shopping_cart = session_cart

    # Retrieve the quantity from the form data
    quantity = int(request.POST.get('quantity', 1))

    # Check if the product is already in the cart
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=shopping_cart, product=product)

    if not item_created:
        # If the item is already in the cart, update the quantity
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity

    cart_item.save()
    messages.success(request, 'Successfully Added')

    return redirect('product_detail', product_id=product_id)


def view_cart(request):
    if request.user.is_authenticated:
        # For authenticated users, use the user's cart
        user = request.user
        shopping_cart, created = ShoppingCart.objects.get_or_create(user=user)
    else:
        # For anonymous users, use the session to store cart information
        session_cart_id = request.session.get('session_cart_id', None)

        if session_cart_id is None:
            # Create a new shopping cart for the session
            session_cart = ShoppingCart()
            session_cart.save()
            request.session['session_cart_id'] = session_cart.id
        else:
            # Retrieve the existing shopping cart
            session_cart = ShoppingCart.objects.get(id=session_cart_id)

        shopping_cart = session_cart

    cart_items = CartItem.objects.filter(cart=shopping_cart)
    categories = Category.objects.all()

    context = {
        'cart_items': cart_items,
        'shopping_cart': shopping_cart,
        'categories': categories,
    }

    return render(request, 'cart/update_cart_item.html', context)


def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'increment':
            cart_item.quantity += 1
        elif action == 'decrement' and cart_item.quantity > 1:
            cart_item.quantity -= 1

        cart_item.save()

    user = request.user

    if user.is_authenticated:
        # For authenticated users, redirect to 'view_cart'
        return redirect('view_cart')
    else:
        # For anonymous users, use the session to store cart information
        session_cart_id = request.session.get('session_cart_id', None)

        if session_cart_id:
            session_cart = ShoppingCart.objects.get(id=session_cart_id)
            return redirect('view_cart')  # Redirect to the cart view

    return redirect('home')  # Redirect anonymous users elsewhere


def checkout(request):
    user = request.user

    if user.is_authenticated:
        shopping_cart, created = ShoppingCart.objects.get_or_create(user=user)
        user_profile = UserProfile.objects.filter(
            user=user).first()
    else:
        # For anonymous users, use the session to store cart information
        session_cart_id = request.session.get('session_cart_id', None)

        if session_cart_id:
            shopping_cart = ShoppingCart.objects.get(id=session_cart_id)

        else:
            return redirect('view_cart')

        user_profile = None  # Anonymous users typically don't have profiles

    cart_items = CartItem.objects.filter(cart=shopping_cart)
    categories = Category.objects.all()

    context = {
        'cart_items': cart_items,
        'shopping_cart': shopping_cart,
        'categories': categories,
        'user_profile': user_profile,
    }

    if cart_items.count() == 0:  # Check if the cart is empty
        messages.error(request,
                       'Your cart is empty. Add items to your'
                       ' cart before checking out.')
        return redirect('view_cart')  # Redirect to the cart view

    return render(request, 'cart/checkout.html', context)


def payment_confirmation(request):
    return render(request, 'payment_confirmation.html')


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    user = request.user

    if user.is_authenticated:
        # For authenticated users, check if the cart item belongs to the user
        if cart_item.cart.user == user:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
        else:
            messages.error(request,
                           'You do not have permission to remove this item.')
    else:
        # For anonymous users, check if the cart item belongs to the session
        session_cart_id = request.session.get('session_cart_id', None)

        if session_cart_id and cart_item.cart.id == session_cart_id:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
        else:
            messages.error(request,
                           'You do not have permission to remove this item.')

    # Redirect back to the cart page
    return redirect('view_cart')


def remove_all_items_from_cart(request):
    user = request.user

    if user.is_authenticated:
        sleep(4)
        # For authenticated users, remove all cart items for the user
        CartItem.objects.filter(cart__user=user).delete()
        messages.success(request, 'Your Order has been Confirmed.')
    else:
        # For anonymous users, remove all cart items for the session
        session_cart_id = request.session.get('session_cart_id', None)

        if session_cart_id:
            try:
                sleep(4)
                shopping_cart = ShoppingCart.objects.get(id=session_cart_id)
                # Delete all cart items associated with the shopping cart
                CartItem.objects.filter(cart=shopping_cart).delete()
                messages.success(request, 'Your Order has been Confirmed.')
            except ObjectDoesNotExist:
                messages.error(request, 'No cart found.')
        else:
            messages.error(request, 'No cart found.')

    # Redirect back to the cart page or another appropriate page
    return redirect('index')

def randomly_generated_products(request):
    products = Product.objects.all()
    num_products = products.count()
    num_samples = min(16, num_products)  # Ensure you're sampling 16 or less products

    random_products = random.sample(list(products), num_samples)

    return render(request, 'wwhg_app/randomly_generated_products.html', {'random_products': random_products})


def fetch_next_holiday():
    country = 'ee'
    year = '2023'
    api_url = f'https://api.api-ninjas.com/v1/holidays?country={country}&year={year}'
    api_key = 'MJFipoF61ofptuuV491RmA==xdzwKQtxoAAGv8xB' # Siia individuaalne API võti

    # Teeb päringu Ninja API-le (Holiday) kokkulepitud formaadis
    response = requests.get(api_url, headers={'X-Api-Key': api_key})

    # kontrollib kas saadi API-lt status kood 200 ,et
    if response.status_code == requests.codes.ok:
        # Saadud Json vastuse teeb ümber listiks, mis sisaldab dicte,
        #list sorditakse date-i järgi, et oleks lihtne loopiga leida tulev esimene kuupäev.
        holiday_data = json.loads(response.content)
        sorted_holidays = sorted(holiday_data, key=lambda x: x['date'])

        current_date = datetime.now()
        next_holiday = None

        for holiday in sorted_holidays:
            holiday_date = datetime.strptime(holiday['date'], '%Y-%m-%d')

            if holiday_date >= current_date:
                next_holiday = holiday
                break

        # Aja arvestamiseks, palju tähtpäevani, hiljem sain aru ,et selle teeb ära ka JS
        # ja teoreetiliselt saaks selle osa ka välja jätta.
        if next_holiday:
            time_remaining = holiday_date - current_date
            days_remaining = time_remaining.days
            hours_remaining, remainder = divmod(time_remaining.seconds, 3600)
            minutes_remaining, seconds_remaining = divmod(remainder, 60)

            # Need siis contentid ,et saaks nende nimedega välja kutsuda.
            return {
                'next_holiday': next_holiday,
                'days_remaining': days_remaining,
                'hours_remaining': hours_remaining,
                'minutes_remaining': minutes_remaining,
                'seconds_remaining': seconds_remaining
            }
        else:
            return {'error_message': "No upcoming holidays found"}

    else:
        return {'error_message': f"Error: {response.status_code}, {response.content}"}


def next_holiday(request):
    next_holiday_data = fetch_next_holiday()
    return render(request, 'wwhg_app/next_holiday.html', next_holiday_data)

