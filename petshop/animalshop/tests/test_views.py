from urllib import response
from django.test import TestCase
from django.urls import reverse
from animalshop.models import Category, Product


class AnimalShopViewTestCase(TestCase):
    def setUp(self) -> None:
        cat = Category.objects.create(name='Views Category')
        Product.objects.create(
            category=cat,
            name='Views Product',
            slug='views-product',
            price=100.00,
            _discount=50.00
        )

    def test_index_view(self):
        """
        New products and all Categories is
        displayed on the landing page.
        """
        cat_ins = Category.objects.all()
        prod_ins = Product.objects.all()

        response = self.client.get(reverse('animalshop:animalshop-LP'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Views Category')
        self.assertContains(response, 'Views Product')
        self.assertQuerysetEqual(response.context['categories'], cat_ins)
        self.assertQuerysetEqual(response.context['products'], prod_ins)
        self.assertTemplateUsed(response, 'animalshop/landing_page.html')

    def test_index_view_return_products(self):
        """
        6 New products and all Categories is
        displayed on the landing page.
        """
        cat_ins = Category.objects.all()
        for x in range(7):
            Product.objects.create(
                category=cat_ins[0],
                name=f'Views Product{x}',
                slug=f'views-product-{x}',
                price=100.00,
                _discount=50.00
            )
        prod_ins = Product.objects.all().order_by('-updated')
        response = self.client.get(reverse('animalshop:animalshop-LP'))

        self.assertQuerysetEqual(response.context['categories'], cat_ins)
        self.assertQuerysetEqual(response.context['products'], prod_ins[:6])
