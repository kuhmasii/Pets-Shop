
from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
def order_created(order_id):
    """
    Task to send an email notification when
    an order is successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order num. {order.id}'
    message = f"""
                Dear {order.first_name},\n\n
                You have sucessfully placed an order.
                Your order ID is {order.id}.
                """
    mail_sent = send_mail(
        subject,
        message,
        'abc@gmail.com',
        [order.email]
    )
    return mail_sent
