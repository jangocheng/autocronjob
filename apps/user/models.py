# -*- coding:utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser
from simple_history.models import HistoricalRecords


class UserProfile(AbstractUser):
    """
    userprofile
    """
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")
    # changed_by = models.ForeignKey('user.UserProfile', null=True, blank=True, on_delete=models.SET_NULL, )
    history = HistoricalRecords(excluded_fields=['first_name', 'is_staff', 'last_name', 'date_joined', 'last_login'])

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username.__str__()
