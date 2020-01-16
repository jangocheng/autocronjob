# -*- coding:utf-8 -*-
__author__ = 'qing.cai@horizon.ai'

from django.http import JsonResponse


def superpermission(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return func(request, *args, **kwargs)
        else:
            return JsonResponse({'status': False, 'message': 'Not allowed. Please request access!'})
    return wrapper