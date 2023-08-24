from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
import datetime
import os


# Create your models here.

def filepath(request, filename):
    old_filename = filename
    time_now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    new_filename = "{}{}".format(time_now, old_filename)
    return os.path.join('uploads/', new_filename)


class Category(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f" Category {self.name}"


class Product(models.Model):
    name = models.TextField(max_length=191, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.TextField(max_length=50, null=False)
    description = models.TextField(max_length=500, null=True)
    image = models.ImageField(upload_to=filepath, null=True, blank=True)

    def __str__(self):
        return f" Product {self.name}"


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(max_length=254, blank=False, unique=True)
    phone_number = models.PositiveIntegerField(max_length=15, blank=False, null=False)
    home_address = models.CharField(max_length=254, blank=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
