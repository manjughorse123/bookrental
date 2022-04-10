from django.conf.urls import url, include

from . import views

app_name = 'invoice'
urlpatterns = [
    
    url(r'^invoicelist/(?P<id>[-\w]+)/$', views.InvoiceView, name='invoicelist'),
]