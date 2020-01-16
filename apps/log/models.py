# -*- coding:utf-8 -*-

from django.db import models


class OperationLog(models.Model):
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
