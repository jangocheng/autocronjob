# -*- coding:utf-8 -*-
__author__ = 'qing.cai@horizon.ai'

import os
import django
from channels.routing import get_default_application

django.setup()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autocronjob.settings")
application = get_default_application()
