from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
import datetime
import os
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re
from decimal import Decimal
from django.contrib.sites.models import Site

# Create your models here.

def filepath(request, filename):
    old_filename = filename
    time_now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    new_filename = "{}{}".format(time_now, old_filename)
    return os.path.join('uploads/', new_filename)


class Category(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f"Category {self.name}"


class Product(models.Model):
    name = models.TextField(max_length=191, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    description = models.TextField(max_length=500, null=True)
    image = models.ImageField(upload_to=filepath, null=True, blank=True)

    def __str__(self):
        return f"Product {self.name}"


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,
                             null=True)
    session_key = models.CharField(max_length=32, blank=True,
                                   null=True)  # For anonymous users
    created_at = models.DateTimeField(auto_now_add=True)

    def get_cart_items(self):
        total_quantity = 0
        cart_items = self.cartitem_set.all()
        for item in cart_items:
            total_quantity += item.quantity
        return total_quantity

    def get_cart_total(self):
        total = Decimal('0.00')
        cart_items = self.cartitem_set.all()
        for item in cart_items:
            total += item.product.price * item.quantity
        return total

    def __str__(self):
        if self.user:
            return f"Shopping Cart for {self.user.username}"
        elif self.session_key:
            return f"Anonymous Shopping Cart ({self.session_key})"
        else:
            return "Empty Shopping Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"CartItem {self.id} in Cart {self.cart.id}"


def validate_phone_number(value):
    if not re.match(r'^[0-9+()-]*$', value):
        raise ValidationError(
            _("Phone number must contain only digits,"
              " plus signs, hyphens, and parentheses."),
            code='invalid_phone_number')


def validate_credit_card_number(value):
    # Remove spaces from the entered card number
    card_number = value.replace(" ", "")

    if not card_number.isnumeric() or len(card_number) != 16:
        raise ValidationError(
            _("Enter a valid 16-digit credit card number."),
            code='invalid_credit_card_number'
        )


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    email = models.EmailField(max_length=254, blank=False, unique=False)
    phone_number = models.CharField(max_length=15, blank=False, null=False,
                                    validators=[validate_phone_number])
    home_address = models.CharField(max_length=254, blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    country = models.CharField(max_length=100, blank=False, null=False,
                               default="Estonia")
    postcode = models.CharField(max_length=10, blank=False, null=False)
    card_name = models.CharField(max_length=100, blank=False, null=False)
    card_number = models.CharField(max_length=16, blank=False, null=False,
                                   validators=[validate_credit_card_number])
    exp_month = models.CharField(max_length=2, blank=False, null=False)
    exp_year = models.CharField(max_length=4, blank=False, null=False)
    cvv = models.CharField(max_length=3, blank=False, null=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # Check if a UserProfile already exists for the user
    if created and not hasattr(instance, 'userprofile'):
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class SiteConfiguration(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE)
    num_random_products = models.PositiveIntegerField(default=16)

    def __str__(self):
        return self.site.name
