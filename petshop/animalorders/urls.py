from django.urls import path
from . import views


app_name = 'animalorders'

urlpatterns = [
    path('create/', views.create_order, name='animalorders-create'),
]
