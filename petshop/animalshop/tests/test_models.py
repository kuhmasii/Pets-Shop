from django.test import TestCase
from animalshop.models import Product, Category


class CategoryTestCase(TestCase):

    def setUp(self) -> None:
        Category.objects.create(
            name='Testing Category'
        )

    def test_category_object_created(self):
        """
        Test checks an object of Category was 
        sucessfully created.
        """
        obj = Category.objects.get(pk=1)
        check = f'Testing Category--- created on ---{obj.updated}'

        self.assertIsInstance(obj, Category)
        self.assertEqual(obj.__str__(), check)

    def test_category_object_not_created(self):
        """
        Test checks if an object of Category is not
        an instance of Category 
        """

        obj = Category.objects.get(pk=1)

        self.assertNotIsInstance('Dummy data', Category)
        self.assertNotEqual(obj.__str__(), 'Dummy data')

    def test_data_for_instance(self):
        """
        Testing an instance data is correct
        """
        ins = Category.objects.get(pk=1)

        self.assertEqual(ins.name, 'Testing Category')

    def test_data_not_for_instance(self):
        """
        Testing an instance data is not correct
        """
        ins = Category.objects.get(pk=1)

        self.assertNotEqual(ins.name, 'This is not your data')

    def test_get_prod_method(self):
        """
        Test checks the get_prod method, should
        return a queryset 
        """
        obj = Category.objects.get(pk=1)
        Product.objects.create(
            category=obj, name='Testing Product', price=100.00, _discount=50.00)

        self.assertEqual(obj.get_prod(obj.id).name, 'Testing Product')
        self.assertEqual(obj.get_prod(obj.id).price, 100.00)

    def test_get_products_method(self):
        """
        Test checks the get_products method, should
        return a queryset 
        """
        obj = Category.objects.get(pk=1)
        Product.objects.create(
            category=obj, name='Testing Product', price=100.00, _discount=50.00)

        self.assertTrue(obj.get_products())
        self.assertQuerysetEqual(
            obj.get_products(), Product.objects.filter(category=obj))


class ProductTestcase(TestCase):
    def setUp(self) -> None:
        cat = Category.objects.create(name='Testing Category')
        Product.objects.create(
            category=cat, name='Testing Product',
            slug='testing-product',
            price=100.00,
            _discount=50.00)

    def test_product_object_created(self):
        """
        Test checks an object of Product was 
        sucessfully created.
        """
        obj = Product.objects.get(pk=1)
        check = 'Testing Product'

        self.assertIsInstance(obj, Product)
        self.assertEqual(obj.__str__(), check)

    def test_product_object_not_created(self):
        """
        Test checks if an object of Product is not
        an instance of Category 
        """

        obj = Product.objects.get(pk=1)

        self.assertNotIsInstance('Dummy data', Product)
        self.assertNotEqual(obj.__str__(), 'Dummy data')

    def test_data_for_instance(self):
        """
        Testing an instance data is correct
        """
        ins = Product.objects.get(pk=1)

        self.assertEqual(ins.name, 'Testing Product')
        self.assertEqual(ins.price, 100.00)
        self.assertNotIsInstance(type(ins.price), float)

    def test_get_absolute_url_method(self):
        """
        Test should return a url route
        """
        obj = Product.objects.get(pk=1)

        self.assertEqual(
            obj.get_absolute_url(), '/product/1/testing-product/'
        )

    def test_discount_method(self):
        """
        Test should return the field discount's value
        """
        obj = Product.objects.get(pk=1)

        self.assertEqual(obj.discount, obj._discount)

    def test_image_method(self):
        """
        Test should return a file path
        """
        obj = Product.objects.get(pk=1)
        obj._image = 'image.png'
        obj.save()

        self.assertEqual(obj.image, '/uploads/image.png')

    def test_no_image_for_image_method(self):
        """
        Test should return an empty string
        """
        obj = Product.objects.get(pk=1)

        self.assertEqual(obj.image, '')
