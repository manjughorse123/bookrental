

from django.conf.urls import url
from . import views
# from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [

    url(r'^(?P<pk>[0-9]+)/$', views.TransactionRUDView.as_view(), name='RUD'),
    url(r'^create/$', views.TransactionCreateView.as_view(), name='RUD'),
    url(r'^order/search/$', views.TransactionOrderSearchView.as_view(), name='search'),
    url(r'^customer/search/$', views.TransactionCustomerSearchView.as_view(), name='search'),
    url(r'^(?P<pk>[0-9]+)/update/$', views.TransactionUpdateView.as_view(), name='Transaction_update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.TransactionDeleteView.as_view(), name='Transaction_delete'),
    url(r'', views.TransactionListView.as_view(), name='Transaction'),

]