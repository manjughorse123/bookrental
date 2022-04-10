from django.conf.urls import include, url
from .import views

app_name = "paytm"
urlpatterns = [
    # Examples:
    url(r'home/', views.home, name='home'),
    url(r'^payment/', views.payment, name='payment'),
    url(r'^response/', views.response, name='response')
]