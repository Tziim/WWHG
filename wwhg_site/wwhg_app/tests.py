from django.test import TestCase
from django.test import TestCase, Client



def test_category_creation():
    category = Category.objects.create(name="Test Category")
    saved_category = Category.objects.get(name="Test Category")
    assert category == saved_category

