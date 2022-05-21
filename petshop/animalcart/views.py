from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from animalshop.models import Product
from .cart import Cart
from .forms import CartProductForm


def detail_product(request):
    cart = Cart(request)
    context = {'cart': cart}
    return render(request, 'animalshop/detail.html', context)


@require_POST
def add_product(request, product_id):
    cart = Cart(request)
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise Http404

    cart_form = CartProductForm(request.POST)
    if cart_form.is_valid():
        data = cart_form.cleaned_data
        cart.add(product=product,
                 quantity=data['quantity'], override_quantity=data['override'])
        return redirect('animalcart:animalcart-detail')


@require_POST
def remove_product(request, product_id):
    cart = Cart(request)
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise Http404
    cart.remove(product)
    return redirect('animalcart:animalcart-detail')
