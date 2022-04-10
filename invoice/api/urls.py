#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Python imports.
import logging

# Django imports.
from django.conf.urls import url, include

# Rest Framework imports.
from rest_framework.routers import DefaultRouter
# Third Party Library imports

# local imports.

#from invoice.swagger import schema_view

from invoice.api import views

# router = DefaultRouter()
# router.register(r'medicines', views.MedicineViewSet)
#router.register(r'users', views.UserViewSet)

urlpatterns = [
    
    url(r'^list_invoice/$', views.InvoiceViewSet.as_view(), name='list_invoice'),
    url(r'^list_invoiceitem/$', views.InvoiceItemViewSet.as_view(), name='list_invoiceitem'),
    url(r'^get_invoice/$', views.InvoiceSearchView.as_view(), name='get_invoice'),
    url(r'^add_invoice/$', views.AddNewInvoice.as_view(), name='add_invoice'),
    url(r'^update_invoice/(?P<id>[0-9]+)/$', views.UpdateInvoice.as_view(), name='update_invoice'),
    url(r'^delete_invoice/(?P<id>[0-9]+)/$', views.InvoiceDeleteView.as_view(), name='delete_invoice'),

]