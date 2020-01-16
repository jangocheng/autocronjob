# -*- coding:utf-8 -*-
__author__ = 'qing.cai@horizon.ai'

from user.models import UserProfile
from rest_framework import serializers
from drf_dynamic_fields import DynamicFieldsMixin
from django.contrib.auth.hashers import make_password


class UserProfileSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    def validate(self, attrs):
        if attrs["password"] != "None":
            attrs["password"] = make_password(attrs["password"])
        else:
            del attrs["password"]
        return attrs

    class Meta:
        model = UserProfile
        fields = '__all__'

