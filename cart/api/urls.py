from django.conf.urls import url
from . import views
# from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [

    url(r'^(?P<pk>[0-9]+)/$', views.CartRUDView.as_view(), name='RUD'),
    url(r'^create/$', views.CartCreateView.as_view(), name='RUD'),
    url(r'^search/$', views.CartSearchView.as_view(), name='search'),
    url(r'^(?P<pk>[0-9]+)/update/$', views.CartUpdateView.as_view(), name='cart_update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.CartDeleteView.as_view(), name='cart_delete'),
    url(r'', views.CartListView.as_view(), name='order'),

]