#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Python imports.
import logging

from django.conf.urls import url
from django.contrib.auth import views as auth_views
from suppliers import views
app_name = 'suppliers'

urlpatterns = [
    url(r'^home/', views.supplierhome, name='supplierhome'),
    url(r'^add_book/', views.insert_book, name='supplieraddbook'),
    url(r'^delete/(?P<isbn_code>\d+)/$',views.delete_book ,name='delete'),
	url(r'^update/(?P<isbn_code>\d+)/$',views.update_book ,name='updated'),
    ]