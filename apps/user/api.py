# -*- coding:utf-8 -*-
__author__ = 'qing.cai@horizon.ai'

from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework import viewsets
from rest_framework import mixins, status

from user.models import UserProfile
from user.serializers import UserProfileSerializer
from utils.audit_record_decorator import user_operation_log_decorator

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


def jwt_response_payload_handler(token, user=None, request=None):
    """
    登录成功后自定义返回
    :param token:
    :param user:
    :param request:
    :return:
    """
    return {
        "status": "ok",
        'user': UserProfileSerializer(user, context={'request': request}).data,
        "token": token
    }


class CustomBackend(ModelBackend):
    """
    自定义认证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class UserProfileViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                         mixins.CreateModelMixin, viewsets.GenericViewSet):

    """
    用户接口
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    @method_decorator(user_operation_log_decorator('添加用户'))
    def create(self, request, *args, **kwargs):
        try:
            super().create(request, *args, **kwargs)
        except Exception as e:
            return JsonResponse({"status": False, "message": "create failed, error:%s" % e},
                                status=status.HTTP_403_FORBIDDEN)
        return JsonResponse({"status": True, "message": "create success!"},
                            status=status.HTTP_201_CREATED)

    @method_decorator(user_operation_log_decorator('更新用户'))
    def update(self, request, *args, **kwargs):
        try:
            super().update(request, *args, **kwargs)
        except Exception as e:
            return JsonResponse({"status": False, "message": "update failed, error:%s" % e},
                                status=status.HTTP_403_FORBIDDEN)
        return JsonResponse({"status": True, "message": "update success!"},
                            status=status.HTTP_200_OK)

    @method_decorator(user_operation_log_decorator('删除用户'))
    def destroy(self, request, *args, **kwargs):
        try:
            super().destroy(request, *args, **kwargs)
        except Exception as e:
            return JsonResponse({"status": False, "message": "delete failed, error:%s" % e},
                                status=status.HTTP_403_FORBIDDEN)
        return JsonResponse({"status": True, "message": "deleted success!"},
                            status=status.HTTP_200_OK)

