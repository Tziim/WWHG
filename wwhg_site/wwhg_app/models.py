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
