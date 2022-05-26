from django.shortcuts import render
from .forms import OrderCreateForm
from .models import OrderItem
from animalcart.cart import Cart


def create_order(request):
	cart = Cart(request)
	form = OrderCreateForm()

	if request.method == 'POST':
		form = OrderCreateForm(request.POST)
		if form.is_valid():
			order = form.save()
			for x in cart:
				OrderItem.objects.create(
					order=order,
					product=x['product'],
					price=x['price'],
					quantity=x['quantity']
					)
				cart.flush()
				context = {'cart':cart, 'form':form}
				return render(request, 'animalorders/checkout.html', context)

	context = {'cart':cart, 'form':form}
	return render(request, 'animalorders/checkout.html', context)