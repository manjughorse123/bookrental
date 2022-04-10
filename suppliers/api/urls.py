from django.conf.urls import url
from .views import *
from . import views

# from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [

    url(r'^(?P<pk>[0-9]+)/$', views.SuppliersRUDView.as_view(), name='RUD'),
    url(r'^create/$', views.SuppliersCreateView.as_view(), name='CRAETERUD'),
    url(r'^search/$', views.SuppliersSearchView.as_view(), name='search'),
    url(r'^(?P<pk>[0-9]+)/update/$', views.SuppliersUpdateView.as_view(), name='supplier_update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.SuppliersDeleteView.as_view(), name='supplier_delete'),
    url(r'', views.SuppliersListView.as_view(), name='supplier_list'),

]