from django.shortcuts import render, redirect
from .payments import gateway, error
from django.http import Http404, HttpResponse
from animalorders.models import Order
from .tasks import payment_completed


def payment_process(request):
    order_id = request.session.get('order_id')
    try:
        order = Order.objects.get(id=1)
        # order = Order.objects.get(id=order_id)
        total_cost = order.get_total_cost()
        client_token = gateway.client_token.generate()
    except (Order.DoesNotExist, error):
        return HttpResponse('This is an error')

    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = gateway.transaction.sale({
            'amount': f'{round(total_cost, 2)}',
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        }
        )
        if result.is_success:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.transaction_id = result.transaction.id
            order.save()
            # launching an asynchronous task
            payment_completed.delay(order.id)

            return redirect('gateways:gateways-completed')
        else:
            return redirect('gateways:gateways-canceled')

    context = {'client_token': client_token,
               'order': order}
    return render(request, 'gateways/payment.html', context)


def payment_completed(request):
    return render(request, 'gateways/completed.html')


def payment_canceled(request):
    return render(request, 'gateways/canceled.html')
