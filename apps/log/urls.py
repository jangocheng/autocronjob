# -*- coding:utf-8 -*-
__author__ = 'qing.cai@horizon.ai'

from django.urls import re_path
from log.views import (OperationLogView, HistoricalUserLog)

urlpatterns = [
    # re_path(r'^log/list/$', OperationLogView.as_view(), name='operationlog'),
    re_path(r'^log/list/$', HistoricalUserLog.as_view(), name='operationlog')
]
