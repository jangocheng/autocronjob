# -*- coding:utf-8 -*-

from django.db import models


class OperationLog(models.Model):
    """
    弃用
    """
    op_user = models.CharField(max_length=20, null=True)
    op_user_ip = models.CharField(max_length=200, null=True)
    op_msg = models.CharField(max_length=50)
    op_object = models.CharField(max_length=200)
    op_time = models.DateTimeField(auto_now=True)
    is_success = models.BooleanField()
    op_failed_msg = models.CharField(max_length=2000, null=True, blank=True)

    class Meta:
        verbose_name = "操作日志"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.op_user

#
# from simple_history import register
# from simple_history.models import HistoricalRecords
# from django_celery_beat.models import IntervalSchedule, PeriodicTask
#
#
# # 这种方式记录第三方组件，默认只能读取到一条历史差异，后面可以在仔细实验一下
# register(IntervalSchedule)
# register(PeriodicTask)


class HistoryLogRecords(models.Model):
    """
    当前使用
    """
    op_user = models.CharField(max_length=20, null=True)
    op_msg = models.TextField()
    op_type = models.CharField(max_length=30)
    op_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "操作日志"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.op_user