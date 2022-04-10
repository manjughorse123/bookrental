from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.conf.urls.static import static
from django.conf import settings

# from user.views import UsersListView, GenerateRandomUserView

from orders import views



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1.0/users/', include(("users.api.urls"), namespace='users-api')),
    url(r'^api/v1.0/order/', include("orders.api.urls")),
    url(r'^api/invoice/', include('invoice.api.urls')), 
    url(r'^api/book/', include('books.api.urls')),
    url(r'^api/supplier/', include('suppliers.api.urls')),
    url(r'^api/manufacturer/', include('manufacturer.api.urls')),
    url(r'^carts/', include('cart.api.urls')),

    url(r'^api/transaction/', include('transactions.api.urls')),

    # url(r'^api/transaction/', include('transaction.api.urls')),
    # url(r'^suppliers/', include('suppliers.urls')), 

    url(r'^invoice/', include(('invoice.urls'),namespace='invoice')), 
    url(r'^orders/', include('orders.urls')),   
    url(r'^book/', include('books.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^paytm/', include('paytm.urls')),
    url(r'^payment/', include('payment.urls')),
    url(r'^payu/', include('payu.urls')),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^users/', include(('users.urls'), namespace='users')),
    url(r'^suppliers/', include('suppliers.urls')),
    url(r'^myorders/(?P<id>\d+)/$', views.myorders_detail, name='myorders_detail'),
    url(r'^myorders/', views.myorders, name='myorders'),
    url(r'^', include(('Home.urls'), namespace='home')),
    # url(r'^userlist/$', views.UsersListView.as_view(), name='users_list'),
    # url(r'^generate/$', views.GenerateRandomUserView.as_view(), name='generate'),
    # url(r'^scrapper/$', views.scrapper, name='scrapper'),



]

from django.conf import settings
from django.conf.urls.static import static



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="BooksRenter API",
        default_version='v1',
        description="BooksRenter API",
        contact=openapi.Contact(email="info@collexatech.com"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns += [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=None),
        name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
]       
