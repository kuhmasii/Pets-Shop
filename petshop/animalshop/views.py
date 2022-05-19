from django.http import HttpResponse
from django.shortcuts import render
from . models import Category, Product


def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()[:6]
    context = {'categories': categories,
               'products': products
               }
    return render(request, 'animalshop/landingpage.html', context)
