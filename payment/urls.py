from django.conf.urls import url
from .import views

app_name = "payment"
urlpatterns = [
    url(r'^process/$', views.process, name='process'),
    url(r'^done/$', views.payment_done, name='done'),    
    url(r'^canceled/$', views.payment_canceled, name='canceled'),
    
    url(r'^success/$', views.payment_success, name='payment_success'),
    url(r'^failure/$', views.payment_failure, name='payment_failure'),
    url('', views.checkout, name='check_out'),

]