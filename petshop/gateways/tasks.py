from io import BytesIO
from msilib.schema import File

from django.http import Http404
from celery import shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from animalorders.models import Order


@shared_task
def payment_completed(order_id):
    """
    Task to send an email notification
    when an order is successfully created.
    """
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        raise Http404

    # creating an INVOICE email
    subject = f'My Petshop - EE INVOICE no.{order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(
        subject, message, 'olaisaiah54@gmail.com', [order.email])

    # generate pdf File
    html = render_to_string('animalorders/pdf.html', {'order': order})
    output = BytesIO()
    weasyprint.HTML(string=html).write_pdf(output,
                                           stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])

    # attaching pdf File
    email.attach(f'Petshoporder_{order.id}.pdf',
                 output.getvalue(), 'application/pdf')
    # sending email
    email.send()
