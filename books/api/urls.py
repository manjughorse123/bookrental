from django.conf.urls import url
from . import views
# from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [
    url(r'^search/$', views.BooksSearchView.as_view(), name='search'),
    url(r'^(?P<pk>[0-9]+)/$', views.BooksRUDView.as_view(), name='create'),
    url(r'^create/$', views.BooksPostView.as_view(), name='post_Create'),
    url(r'^(?P<pk>[0-9]+)/update/$', views.BooksUpdateView.as_view(), name='post_update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.BooksDeleteView.as_view(), name='post_delete'),
    url(r'$', views.BooksListView.as_view(), name='post_Create'),


]
