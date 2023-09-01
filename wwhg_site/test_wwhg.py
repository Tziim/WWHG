from django.test import TestCase
from django.urls import reverse
from wwhg_app import views
from wwhg_site.urls import *


@views
class TestIndexView(TestCase):
    def test_index(self):
        response = self.client.get(reverse(
            'index'))  # Replace 'index' with the actual name of your index view in urls.py
        self.assertEqual(response.status_code,
                         200)  # Check if the view returns a 200 status code
        # Add more assertions to check the content or context as needed

# class TestAllProductsView(TestCase):
#     def test_all_products_view(self):
#         response = self.client.get(reverse(
#             '/admin'))  # Replace 'all_products' with your view name
#         self.assertEqual(response.status_code,
#                          200)  # Check if the view returns a 200 status code
#         # Add more assertions to check the content or context as needed
#

# class TestProductDetailView(TestCase):
#     def test_product_detail_view(self):
#         product_id = 1  # Replace with a valid product ID
#         response = self.client.get(reverse('product_detail', args=[
#             product_id]))  # Replace 'product_detail' with your view name
#         self.assertEqual(response.status_code,
#                          200)  # Check if the view returns a 200 status code
#         # Add more assertions to check the content or context as needed
#
#
# class TestRegisterView(TestCase):
#     def test_register_view(self):
#         response = self.client.get(
#             reverse('register'))  # Replace 'register' with your view name
#         self.assertEqual(response.status_code,
#                          200)  # Check if the view returns a 200 status code
#         # Add more assertions to check the content or context as needed
#
#
# class TestSearchView(TestCase):
#     def test_search_view(self):
#         response = self.client.get(reverse(
#             'search_view'))  # Replace 'search_view' with your view name
#         self.assertEqual(response.status_code,
#                          200)  # Check if the view returns a 200 status code
#         # Add more assertions to check the content or context as needed
