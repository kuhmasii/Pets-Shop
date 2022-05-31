from django.shortcuts import render, redirect
from .forms import OrderCreateForm
from .tasks import order_created
from animalcart.cart import Cart
from django.urls import reverse
from .models import OrderItem


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
                # lauch ascyn task
                order_created.delay(order.id)

                # setting the order in current session
                request.session['order_id'] = order.id
                # redirecting to payment gateway
                return redirect(reverse('gateways:gateways-payment'))

    context = {'cart': cart, 'form': form}
    return render(request, 'animalorders/checkout.html', context)
