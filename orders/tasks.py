from celery import task
from django.core.mail import send_mail
from .models import OrderAddress

@task
def order_created(order_id):
    # import pdb;pdb.set_trace()
    """
    Task to send an e-mail notification when an order is successfully created.
    """
    # import pdb;pdb.set_trace()
    order = OrderAddress.objects.get(id=order_id)
    subject = 'Order no. {}'.format(order.id)
    message = 'Dear {},\n\nYou have successfully placed an order. Your order id is {}.'.format(order.first_name,
                                                                             order.id)
    mail_sent = send_mail(subject, message, 'admin@gmail.com', [order.email])
    return mail_sent
