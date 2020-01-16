# -*- coding:utf-8 -*-
__author__ = 'qing.cai@horizon.ai'

from rest_framework import serializers
from log.models import OperationLog


class OperationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationLog
        fields = '__all__'
