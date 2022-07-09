from animalshop.models import Product, Category
from django.test import TestCase
from django.urls import reverse
from django.conf import settings


class CartTestCase(TestCase):

    def setUp(self) -> None:

        cat = Category.objects.create(name='Testing Category')
        for x in range(10):
            Product.objects.create(
                category=cat,
                name=f'Testing Product{x}',
                slug=f'testing-product{x}',
                price=100.00,
                _discount=50.00
            )

    def test_cart_product_view(self):
        """
        Test that the cart product view returns a response.
        """
        response = self.client.get(reverse('animalcart:animalcart-detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/detail.html')

    def test_add_product_view(self):
        """
        Test that the add_product view should update the product in the 
        cart quantity and redirect to cart_product view.
        """
        ins = Product.objects.get(id=3)
        before_session = self.client.session.load()

        response = self.client.post(
            reverse('animalcart:animalcart-add', args=(ins.id,)),
            data={'quantity': 5, 'override': True}
        )
        after_session = self.client.session.pop('cart')
        session = response.wsgi_request.session.pop('cart')

        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(session, before_session)
        self.assertEqual(session, after_session)
        self.assertEqual(session[str(ins.id)]['quantity'], 5)
        self.assertEqual(session[str(ins.id)]['price'], '100.00')

    def test_remove_product_view(self):
        """
        Test that remove_product view should delete the product from
        the cart and redirect to cart_product view.
        """
        ins = Product.objects.get(id=5)
        self.client.post(
            reverse('animalcart:animalcart-add', args=(ins.id,)),
            data={'quantity': 10, 'override': True}
        )
        session_bef = self.client.session.load()

        response = self.client.post(
            reverse('animalcart:animalcart-remove', args=(ins.id,)))

        session_aft = self.client.session.load()

        self.assertEqual(response.status_code, 302)
        self.assertFalse(session_aft['cart'])
        self.assertTrue(session_bef['cart'])
