from django.urls import path
from . import views

app_name = 'animalcart'

urlpatterns = [
    path('', views.cart_product, name='animalcart-detail'),
    path('add/<int:product_id>/', views.add_product, name='animalcart-add'),
    path('remove/<int:product_id>/',
         views.remove_product, name='animalcart-remove'),


]
