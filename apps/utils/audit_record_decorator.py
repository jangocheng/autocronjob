# -*- coding:utf-8 -*-
__author__ = 'qing.cai@horizon.ai'

from django_celery_beat.models import IntervalSchedule, CrontabSchedule, PeriodicTask
from user.models import UserProfile
from log.models import OperationLog
import json
import django
import re

django.setup()


class MyEncoder(json.JSONEncoder):
    def default(self, obj) -> json:
        """
        只要检查到了是bytes类型的数据就把它转为str类型
        :param obj:
        :return:
        """
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


def user_operation_log_decorator(para: str) -> object:
    """
    用户审计日志
    :param para:
    :return:
    """
    def operationlog_fun(func: type) -> object:
        def wrapper(request, *args, **kwargs) -> object:
            op_msg = para
            if op_msg == '删除用户':
                username = UserProfile.objects.get(id=kwargs.get('pk')).username
            else:
                username = json.loads(request.body)["username"]
            result = func(request, *args, **kwargs)
            if re.search(r'^2|3[0-9]\d+', str(result.__dict__['status_code'])):
                op_failed_msg = None
                is_success = True
            else:
                is_success = False
                op_failed_msg = json.loads(MyEncoder().default(result.__dict__["_container"][0]))
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            OperationLog.objects.create(
                op_user=request.user,
                op_user_ip=ip,
                op_msg=op_msg,
                op_object=username,
                is_success=is_success,
                op_failed_msg=op_failed_msg if op_failed_msg else None
            )
            return result
        return wrapper
    return operationlog_fun


def dag_operation_log_decorator(para):
    """
    任务审计日志
    :param para:
    :return:
    """
    def operation_log_fun(func):
        def wrapper(request, *args, **kwargs):
            op_msg = para

            if op_msg == '删除Crontab任务':
                username = PeriodicTask.objects.get(id=kwargs.get('pk')).name
                result = func(request, *args, **kwargs)
                if re.search(r'^2|3[0-9]\d+', str(result.__dict__['status_code'])):
                    op_failed_msg = None
                    is_success = True
                else:
                    is_success = False
                    op_failed_msg = json.loads(MyEncoder().default(result.__dict__["_container"][0]))
            elif op_msg == '删除Crontab间隔' or op_msg == '删除Interval间隔':
                if op_msg == '删除Crontab间隔':
                    crontab_obj = CrontabSchedule.objects.get(id=kwargs.get('pk'))
                    username = "%s %s %s %s %s (m/h/d/dM/MY)" % (
                        crontab_obj.minute, crontab_obj.hour, crontab_obj.day_of_month,
                        crontab_obj.month_of_year, crontab_obj.day_of_week
                    )
                else:
                    interval_obj = IntervalSchedule.objects.get(id=kwargs.get('pk'))
                    username = "every %s %s" % (interval_obj.every, interval_obj.period)
                result = func(request, *args, **kwargs)
                if re.search(r'^2|3[0-9]\d+', str(result.__dict__['status_code'])):
                    op_failed_msg = None
                    is_success = True
                else:
                    is_success = False
                    op_failed_msg = json.loads(MyEncoder().default(result.__dict__["_container"][0]))

            elif op_msg == '创建Crontab间隔' or op_msg == '更新Crontab间隔':
                result = func(request, *args, **kwargs)
                minute, hour, day_of_month, month_of_year, day_of_week = '', '', '', '', ''
                for i in MyEncoder().default(request.body).split('&'):
                    if "minute=" in i:
                        minute = i.split('=')[1]
                    elif "hour=" in i:
                        hour = i.split('=')[1]
                    elif "day_of_week=" in i:
                        day_of_week = i.split('=')[1]
                    elif "day_of_month=" in i:
                        day_of_month = i.split('=')[1]
                    elif "month_of_year=" in i:
                        month_of_year = i.split('=')[1]
                username = "%s %s %s %s %s (m/h/d/dM/MY)" % (minute, hour, day_of_month, month_of_year, day_of_week)
                try:
                    if result.__dict__.__contains__('_is_rendered'):
                        op_failed_msg = "_is_rendered is false"
                        is_success = False
                    else:
                        op_failed_msg = None
                        is_success = True
                except Exception as e:
                    op_failed_msg = e
                    is_success = False
            elif op_msg == '创建Interval间隔' or op_msg == '更新Interval间隔':
                result = func(request, *args, **kwargs)
                every, period = '', ''
                for i in MyEncoder().default(request.body).split('&'):
                    if "every=" in i:
                        every = i.split('=')[1]
                    elif "period=" in i:
                        period = i.split('=')[1]
                username = "every %s %s" % (every, period)
                try:
                    if result.__dict__.__contains__('_is_rendered'):
                        op_failed_msg = "_is_rendered is false"
                        is_success = False
                    else:
                        op_failed_msg = None
                        is_success = True
                except Exception as e:
                    op_failed_msg = e
                    is_success = False
            else:
                result = func(request, *args, **kwargs)
                username = None
                for i in MyEncoder().default(request.body).split('&'):
                    if "name=" in i:
                        username = i.split('=')[1]
                try:
                    if result.__dict__.__contains__('_is_rendered'):
                        op_failed_msg = "_is_rendered is false"
                        is_success = False
                    else:
                        op_failed_msg = None
                        is_success = True
                except Exception as e:
                    op_failed_msg = e
                    is_success = False
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            OperationLog.objects.create(
                op_user=request.user,
                op_user_ip=ip,
                op_msg=op_msg,
                op_object=username if username else "error",
                is_success=is_success,
                op_failed_msg=op_failed_msg if op_failed_msg else None
            )
            return result
        return wrapper
    return operation_log_fun
