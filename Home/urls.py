#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Python imports.
import logging

# Django imports.
from django.conf.urls import url

# Rest Framework imports.

# Third Party Library imports

# local imports.
from Home import views
app_name = 'Home'

urlpatterns = [

    url(r'^$', views.cartItem.home, name='mainpage'),
  
]