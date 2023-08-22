from django.shortcuts import render,redirect , get_object_or_404
from .forms import RegisterForm
from .models import Product, Category
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .models import UserProfile
from .forms import UserProfileEditForm
from django.contrib.auth.mixins import LoginRequiredMixin


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

    # Retrieve all categories for the menu
    categories = Category.objects.all()

    context = {
        'product': product,
        'categories': categories,
    }

    return render(request, 'wwhg_app/shop/product_detail.html', context)


def category_detail(request, pk):
    # Retrieve the category object using the pk parameter
    category = Category.objects.get(pk=pk)

    categories = Category.objects.all()

    # You can add more logic here if needed

    return render(request, 'wwhg_app/index.html',
                  {'category': category, 'categories': categories})


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


class UserProfileEditView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileEditForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('edit_profile')

    def get_object(self):
        return self.request.user.userprofile

    def form_valid(self, form):
        # Update the user profile with the form data
        user_profile = form.save(commit=False)
        user_profile.user = self.request.user
        user_profile.save()
        return super().form_valid(form)
