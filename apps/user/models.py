# -*- coding:utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    userprofile
    """
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name="邮箱")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username.__str__()
