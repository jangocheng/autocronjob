# -*- coding:utf-8 -*-
__author__ = 'qing.cai@horizon.ai'

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
