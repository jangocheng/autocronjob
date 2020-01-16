# -*- coding:utf-8 -*-
__author__ = 'qing.cai@horizon.ai'

from rest_framework import viewsets
from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from log.serializers import OperationLogSerializer
from log.models import OperationLog


class OpLogPagination(PageNumberPagination):
    """
    审计日志drf 分页
    """
    page_size = 5
    page_size_query_param = 'iDisplayLength'
    page_query_param = 'p'
    max_page_size = 50


class OpLogViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = OperationLog.objects.all().order_by('-op_time')
    serializer_class = OperationLogSerializer
    pagination_class = OpLogPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('op_user', 'is_success')
