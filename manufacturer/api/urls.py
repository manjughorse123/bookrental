from __future__ import unicode_literals
# Python imports.
import logging

# Django imports.
from django.conf.urls import url, include

# Rest Framework imports.
from rest_framework.routers import DefaultRouter
# Third Party Library imports

# local imports.
from manufacturer.api.views import (
                          	ManufacturerViewSet,
                         	ManufacturerSearchView,
                          	AddNewManufacturer,
                          	UpdateManufacturer,
                          	ManufacturerDeleteView,
                          	)
#from medicine.swagger import schema_view

from manufacturer.api import views

# router = DefaultRouter()
# router.register(r'', views.ManufacturerViewSet)
# router.register(r'create/',views.AddNewManufacturer)

urlpatterns = [
    url(r'^list_manufacturer/$', views.ManufacturerViewSet.as_view(), name='list_manufacturer'),
    url(r'^get_manufacturer/$', views.ManufacturerSearchView.as_view(), name='get_manufacturer'),
    url(r'^add_manufacturer/$', views.AddNewManufacturer.as_view(), name='add_manufacturer'),
    url(r'^update_manufacturer/(?P<id>[0-9]+)/$', views.UpdateManufacturer.as_view(), name='update_manufacturer'),
    url(r'^delete_manufacturer/(?P<id>[0-9]+)/$', views.ManufacturerDeleteView.as_view(), name='delete_manufacturer'), 
    
]