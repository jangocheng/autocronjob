# -*- coding:utf-8 -*-
__author__ = 'qing.cai@horizon.ai'

from rest_framework import serializers
from django_celery_beat.models import MailAddress, WebhookUrl


class MailAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailAddress
        fields = '__all__'


class WebhookUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookUrl
        fields = '__all__'


