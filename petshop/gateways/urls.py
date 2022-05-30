from django.urls import path
from . import views

app_name = 'gateways'

urlpatterns = [
	path("", views.payment_process, name='gateways-payment'),
	path("completed/", views.payment_completed, name='gateways-completed'),
	path("canceled/", views.payment_canceled, name='gateways-canceled'),

]