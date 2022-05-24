from django.urls import path
from . import views

app_name = 'animalshop'

urlpatterns = [
    path('', views.index, name='animalshop-LP'),
    path('collections/', views.products, name='animalshop-list'),
    path('<int:category_id>/<slug:category_slug>/',
         views.product_by_cate, name='animalshop-CL'),
    path('<int:detail_id><slug:detail_slug>/',
         views.detail, name='animalshop-detail'),
]
