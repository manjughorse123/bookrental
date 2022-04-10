from django.conf.urls import url
from . import views
# from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [

    url(r'^(?P<pk>[0-9]+)/$', views.OrderRUDView.as_view(), name='RUD'),
    url(r'^create/$', views.OrderCreateView.as_view(), name='create_order'),
    url(r'^search/$', views.OrderSearchView.as_view(), name='search'),
    url(r'^(?P<pk>[0-9]+)/update/$', views.OrderUpdateView.as_view(), name='order_update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.OrderDeleteView.as_view(), name='order_delete'),
    url(r'', views.OrderListView.as_view(), name='order'),

]