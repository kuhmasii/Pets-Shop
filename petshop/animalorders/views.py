from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from .models import OrderItem, Order
from .forms import OrderCreateForm
from django.conf import settings
from .tasks import order_created
from animalcart.cart import Cart
from django.urls import reverse
import weasyprint


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


@staff_member_required
def admin_order_pdf(request, order_id):
    try:
        # order = Order.objects.get(id=1)
        order = Order.objects.get(id=order_id)
        items = order.order_items.all()
    except Order.DoesNotExist:
        raise Http404

    context = {'order': order, 'items': items}
    html = render_to_string('animalorders/pdf.html', context)
    response = HttpResponse(
        content_type='application/pdf',
        headers={
            'Content-Disposition': f'filename={order.id}.pdf'
        }
    )
    weasyprint.HTML(string=html).write_pdf(
            response, stylesheets=[
                weasyprint.CSS('static/css/pdf.css')
                ]
            )
    return response
