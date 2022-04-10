from django.conf.urls import url
from . import views
# from rest_framework_jwt.views import refresh_jwt_token
app_name="books"

urlpatterns = [
    url(r'auto/$', views.auto_search, name='auto_search'),
    url(r'author/$', views.author_search, name='author_search'),
    url(r'search/', views.search, name='search_books'),
    url(r'search1/', views.search1, name='search_books'),
    url(r'home/$', views.home, name='home'),
    url(r'book_path/$', views.book_path, name='book_path'),
    url(r'^(?P<isbn_code>\d+)/$', views.books_detail, name='books_detail'),
    # url('', views.search, name='search_books'),

]