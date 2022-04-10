#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Python imports.
import logging

# Django imports.
from django.conf.urls import url
from django.contrib.auth import views as auth_views
# Rest Framework imports.

# Third Party Library imports

# local imports.
from users import views
app_name = 'users'

urlpatterns = [
    url(r'^signup/', views.SignUp, name='signup'),

    url(r'^logout/', views.Logout, name='logout'),
    url(r'^login/', views.login_user, name='login_user'),
    url(r'^register/', views.register_user, name='register_user'),
    url(r'^find_books/', views.find_books, name='find_books'),
    url(r'^find_book/', views.find_book, name='find_book'),
    url(r'^new_search/', views.new_search, name='new_search'),
    url(r'^(?P<isbn_code>[-\w]+)/$', views.new_search,
        name='product_list_by_category'),
    # url('password_reset/', auth_views.PasswordResetView.as_view(), {'template_name':'registration/password_reset_form.html'}, name='password_reset'),
    # # url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    # url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     auth_views.password_reset_confirm, name='password_reset_confirm'),
    # url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url('password_reset/', auth_views.PasswordResetView.as_view(),
        name='password_reset'),
    url('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(),  name='password_reset_confirm'),
    url('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),


    url(r'^account_activation_sent/$', views.account_activation_sent,
        name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
