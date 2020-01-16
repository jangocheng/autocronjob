# -*- coding:utf-8 -*-
__author__ = 'qing.cai@horizon.ai'

from django.urls import path, re_path, include
from user.views import (LoginView, LogoutView, UserListView, UserCreateView)


urlpatterns = [
    re_path(r'^login/$', LoginView.as_view(), name='login'),
    re_path(r'^logout/$', LogoutView.as_view(), name='logout'),
    re_path(r'^user/$', UserListView.as_view(), name='user_list'),
    re_path(r'^user/create/$', UserCreateView.as_view(), name='user_add')
]

