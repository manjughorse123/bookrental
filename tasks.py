from celery import shared_task
import logging
 
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
# from Eatburp.celery import app
from django.contrib.auth.models import User

# @shared_task
def add(a, b):
    return (a+b)

 
# @app.task
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
            'Verify your Eatburp account',
            'Follow this link to verify your account: '
                'http://localhost:8000%s' % reverse('users-api:verify', kwargs={'uuid': str(user.verification_uuid)}),
            'settings.EMAIL_HOST_USER',
            ['abc91@gmail.com'],
            fail_silently=False,
        )
    except User.DoesNotExist:
        logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)