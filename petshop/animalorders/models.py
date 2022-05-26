from django.db import models
from animalshop.models import Product

class Order(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.EmailField()
	# phone_number
	company = models.CharField(max_length=50)
	# customer model should be created
	#shipping address model should be created
	address = models.CharField(max_length=200)
	# country
	city = models.CharField(max_length=20)
	# state
	postal_code = models.CharField(max_length=20) 
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)
	paid = models.BooleanField(default=False)

	class Meta:
		ordering = ('-updated',)

	def __str__(self):
		return f'Order of {self.id}'

	def get_total_cost(self):
		orderitem = self.order_items.all()
		return sum(x.get_cost() for x in orderitem)


class OrderItem(models.Model):
	order = models.ForeignKey(Order, related_name='order_items',
				on_delete=models.CASCADE)

	product = models.ForeignKey(Product, related_name='order_product',
				on_delete=models.CASCADE)

	price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField(default=1)

	def __str__(self):
		return str(self.id)

	def get_cost(self):
		return self.price * self.quantity