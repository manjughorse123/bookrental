from django.conf.urls import url
from .import views

app_name = "payu"
urlpatterns = [
   
    url(r'^success/$', views.success, name='payment_success'),
    url(r'^failure/$', views.failure, name='payment_failure'),
    url('', views.Home, name='home'),

]