from django.test import TestCase
from django.urls import reverse
from .models import Product, Category


class ModelsTestCase(TestCase):
    def setUp(self):
        # Set up your test data here
        self.category = Category.objects.create(name="Test")
        self.product = Product.objects.create(
            name="Test",
            category=self.category,
            price=69.9,
            description="Test"
        )

    def test_user_profile_edit_view(self):
        # Assume you have logged in or created a user session for testing

        response = self.client.post('/edit_profile/',
                                    data={})
        self.assertEqual(response.status_code, 302)

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_product_str_method(self):
        product = Product.objects.get(name="Test")
        self.assertEqual(str(product), "Product Test")

    def test_category_str_method(self):
        category = Category.objects.get(name="Test")
        self.assertEqual(str(category), "Category Test")