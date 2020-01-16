# -*- coding:utf-8 -*-
__author__ = 'qing.cai@horizon.ai'

from django.urls import re_path
from log.views import (OperationLogView)

urlpatterns = [
    re_path(r'^log/list/$', OperationLogView.as_view(), name='operationlog'),
]
