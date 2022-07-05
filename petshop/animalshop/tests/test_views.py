from django.db.models import Max
from django.test import TestCase
from django.urls import reverse
from requests import Response
from animalshop.models import Category, Product


class AnimalShopViewTestCase(TestCase):
    def setUp(self) -> None:
        cat = Category.objects.create(
            name='Views Category',
            slug='views-category')
        for x in range(7):
            Product.objects.create(
                category=cat,
                name=f'Views Product{x}',
                slug=f'views-product-{x}',
                price=100.00,
                _discount=50.00
            )

    def test_index_view(self):
        """
        6 New products and all Categories is
        displayed on the landing page.
        """
        cat_ins = Category.objects.all()
        prod_ins = Product.objects.all().order_by('-updated')

        response = self.client.get(reverse('animalshop:animalshop-LP'))

    def test_index_view_with_no_data(self):
        """
        Testing index with no queryset should
        return a sentence that shows no data.
        """
        cat_ins = Category.objects.all()
        for x in cat_ins:
            x.delete()
        prod_ins = Product.objects.all().order_by('-updated')
        for x in prod_ins:
            x.delete()

        response = self.client.get(reverse('animalshop:animalshop-LP'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Opps! No Categories for Products yet(')
        self.assertQuerysetEqual(response.context['categories'], [])
        self.assertQuerysetEqual(response.context['products'], [])
        self.assertTemplateUsed(response, 'animalshop/landing_page.html')

    def test_product_view(self):
        """
        Tests should return all available products in
        the database.
        """
        products = Product.objects.all().order_by('-updated')
        response = self.client.get(reverse('animalshop:animalshop-list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Views Product4')
        self.assertQuerysetEqual(response.context['products'], products)
        self.assertTemplateUsed(response, 'animalshop/shop_page.html')

    def test_product_view_with_no_data(self):
        """
        Tests with no queryset should
        return a sentence that shows no data..
        """
        products = Product.objects.all().order_by('-updated')
        for x in products:
            x.delete()
        response = self.client.get(reverse('animalshop:animalshop-list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Opps! Product is not yet added :)')
        self.assertQuerysetEqual(response.context['products'], [])
        self.assertTemplateUsed(response, 'animalshop/shop_page.html')

    def test_product_by_cate_view(self):
        """
        Testing product_by_cate view with a correct Id.
        """
        cat = Category.objects.get(pk=1)
        response = self.client.get(
            reverse('animalshop:animalshop-CL',
                    args=[cat.id, cat.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual([response.context['category']], [cat])
        self.assertContains(response, cat.get_products()[0])
        self.assertTemplateUsed(response, 'animalshop/categorylist.html')

    def test_product_by_cate_view_with_wrong_pk(self):
        """
        Testing product_by_cate view with wrong Id.
        """
        max_id = Category.objects.all().aggregate(Max('id'))['id__max']
        response = self.client.get(
            reverse('animalshop:animalshop-CL',
                    args=[max_id + 1, 'views-category']))
        self.assertEqual(response.status_code, 404)

    def test_detail_view(self):
        """
        Testing detail view with a correct Id.
        """
        prod = Product.objects.get(pk=1)
        response = self.client.get(prod.get_absolute_url())
        fields = response.context['cartform'].fields

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, prod.name)
        self.assertQuerysetEqual([response.context['product']], [prod])
        self.assertTemplateUsed(response, 'animalshop/detail.html')
        self.assertIn('quantity', fields)

    def test_detail_with_wrong_pk(self):
        """
        Testing detail view with wrong Id.
        """
        max_id = Product.objects.all().aggregate(Max('id'))['id__max']
        response = self.client.get(
            reverse('animalshop:animalshop-CL',
                    args=[max_id + 1, 'views-product0']))
        self.assertEqual(response.status_code, 404)
