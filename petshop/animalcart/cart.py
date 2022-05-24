from decimal import Decimal
from django.conf import settings
from animalshop.models import Product


class Cart(object):
    def __init__(self, request) -> None:
        """
        Initialize the cart.
        """
        self.session = request.session

        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # do something
            cart = self.session[settings.CART_SESSION_ID] = {}
        # self.cart will return a dictionary
        self.cart = cart

    def __iter__(self):
        """
        Iterating over all the items in the cart and 
        getting the products from database
        """
        all_product_ids = self.cart.keys()
        # getting all products objects and adding them to the cart
        all_products = Product.objects.filter(id__in=all_product_ids)
        cart = self.cart.copy()
        for prod in all_products:
            cart[str(prod.id)]['product'] = prod

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        getting all the sum of quantity in the cart
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            # storing the temporary data in session
            self.cart[product_id] = {
                'quantity': 0, 'price': str(product.price)
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # This makes sure the session gets saved
        self.session.modified = True

    def remove(self, product):
        '''
        Remove a product from the cart.
        '''
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """
        Remove all cart data from the current session
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity'] for item in self.cart.values()
        )
