from django.http import Http404
from django.shortcuts import render
from . models import Category, Product


def index(request):
    categories = Category.objects.all()
    # calling out the queryset like this makes it cacheable
    queryset = Product.objects.all().order_by('-updated')
    products = [prod for prod in queryset][:6]

    context = {'categories': categories, 'products': products}

    return render(request, 'animalshop/index.html', context)


def products(request):
    products = Product.objects.all().order_by('-updated')
    context = {'products': products}

    return render(request, 'animalshop/list.html', context)


def product_by_cate(request, category_id=None, category_slug=None):
    try:
        category = Category.objects.get(id=category_id, slug=category_slug)
    except Category.DoesNotExist:
        raise Http404
    context = {'category': category}
    return render(request, 'animalshop/categorylist.html', context)


def detail(request, detail_id=None, detail_slug=None):
    try:
        product = Product.objects.get(id=detail_id, slug=detail_slug)
    except Product.DoesNotExist:
        raise Http404
    context = {"product": product}
    return render(request, 'animalshop/detail.html', context)
