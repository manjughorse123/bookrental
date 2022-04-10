from celery import task
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
import logging 
from django.urls import reverse
from django.contrib.auth import get_user_model
from BooksRenter.celery import app
import string
from user.models import User
from django.utils.crypto import get_random_string
from celery import shared_task

@task
def user_created(pk):
    """
    Task to send an e-mail notification when an order is successfully created.
    """
    # import   pdb;pdb.set_trace()
    user        = MyUser.objects.get(id=pk)
    subject     = 'MyUser no. {}'.format(user.id)
    message     = 'Dear {},\n\nYou have successfully login. Your user id is {}.'.format(user.first_name,
                                                                             user.id)
    mail_send   = send_mail(subject, message, 'wadbudenvn19@gmail.com', [user.email], fail_silently=False,)
    
    return mail_send





@shared_task
def create_random_user_accounts(total):
    import pdb;pdb.set_trace()
    for i in range(total):
        phone_number = 'user_{}'.format(get_random_string(10, string.ascii_letters))
        email = '{}@example.com'.format(phone_number)
        password = get_random_string(50)
        MyUser.objects.create_user(phone_number=phone_number, email=email, password=password)
    return '{} random users created with success!'.format(total)



@shared_task
def add(a, b):
    return (a+b)


@app.task
def send_verification_email(user_id):
    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
        # current_site = get_current_site(request)
               
            #     subject = 'Thank you for registering to our site'
               
            #    # message = ' it  means a world to us '
            #     message = render_to_string('send/index2.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token':account_activation_token.make_token(user),
            # })
            #     from_email = settings.EMAIL_HOST_USER
            #     recipient_list = ['manjughorse91@gmail.com']
            #     #import pdb; pdb.set_trace()
            #     send_mail( subject=subject, message=message, from_email=from_email, recipient_list=recipient_list,fail_silently=False )
               # send_mail('hii', 'hemll','manjucollexa@gmail.com',['manjughorse91@gmail.com'], fail_silently=False)
        send_mail(
            'Verify your OnlinePharma account',
            'Follow this link to verify your account: '
                'http://localhost:8000%s' % reverse('users-api:verify', kwargs={'uuid': str(user.verification_uuid)}),
            'settings.EMAIL_HOST_USER',
            ['abc91@gmail.com'],
            fail_silently=False,
        )
    except User.DoesNotExist:
        logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)
