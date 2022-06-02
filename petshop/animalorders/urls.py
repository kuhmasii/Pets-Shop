from django.urls import path
from . import views


app_name = 'animalorders'

urlpatterns = [
    path('create/', views.create_order, name='animalorders-create'),
    path('admin/order/<int:order_id>/pdf/',
         views.admin_order_pdf, name='animalorders-pdf')
]
