from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class Routetesting(TestCase):
    """Test the views of 'searchapp' app."""
    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
    def test_product_page(self):
        response = self.client.get(reverse('product'))
        self.assertEqual(response.status_code, 200)
    def test_account_page(self):
        response = self.client.get(reverse('myaccount'))
        self.assertEqual(response.status_code, 200)

