from django.test import TestCase

from .models import Product, Category


class ModelsTestCase(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Test")
        self.product = Product.objects.create(
            name="Test",
            category=self.category,
            price=69.9,
            description="Test"

        )

    def test_creation(self):
        pass