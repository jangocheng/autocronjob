# -*- coding:utf-8 -*-
__author__ = 'qing.cai@horizon.ai'


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autocronjob.settings")
import django
django.setup()
from user.models import UserProfile

username = 'admin'
password = '123456'
email = ''

if UserProfile.objects.filter(username=username).count() == 0:
    try:
        UserProfile.objects.create_superuser(username, email, password)
        print('Superuser created succeed.')
    except Exception:
        print('Superuser created failed.')
else:
    print('Superuser creation skipped.')
