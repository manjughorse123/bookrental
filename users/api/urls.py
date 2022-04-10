#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Python imports.
import logging

# Django imports.
from django.conf.urls import url

# Rest Framework imports.

from users.api.views import *
from users.swagger import schema_view

app_name = 'users'

urlpatterns = [
    url(r'^register/$', RegistrationAPIView.as_view(), name='register-api'),
    url(r'^login/$', LoginView.as_view(), name='login-api'),
    url(r'^logout/$', LogoutView.as_view(), name='logout-api'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        ActivateApi.as_view(), name='activate'),
    url(r'^verify/(?P<uuid>[a-z0-9\-]+)/$', Verify.as_view(), name='verify'),
    url(r'^signup/$', SignupAPIView.as_view(), name='sign_up'),
    url(r'^signin/$', LoginAPIView.as_view(), name='sign_in'),

    url(r'^GetOtp/$', GetOtp.as_view(), name='send_otp'),
    url(r'^verifyotp/$', VerifyOtp.as_view(), name='check_otp'),
    url(r'^refresh_token/$', RefreshJwtToken.as_view(), name='refresh_token'),

]
