from django.conf.urls import url
from . import views

app_name = "cart"
urlpatterns = [
    url(r'^add/(?P<isbn_code>\d+)/$', views.cart_add, name='cart_add'),
    # url(r'^remove/', views.cart_remove, name='cart_remove'),
    url(r'^remove/(?P<isbn_code>\d+)/$', views.cart_remove, name='cart_remove'),
    url(r'^rent/(?P<isbn_code>\d+)/$', views.rent_book, name='rent_book'),
    url(r'^$', views.cart_detail, name='cart_detail'),
    
]
