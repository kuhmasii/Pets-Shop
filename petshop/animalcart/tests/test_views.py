from django.test import TestCase
from django.urls import reverse


class CartTestCase(TestCase):
    def test_cart_product_view(self):
        """
        Test that the cart product view returns a response.
        """
        response = self.client.get(reverse('animalcart:animalcart-detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/detail.html')
