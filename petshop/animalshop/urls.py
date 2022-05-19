from django.urls import path
from . import views

app_name = 'animalshop'

urlpatterns = [
    path('', views.index, name='animalshop-LP'),
]
