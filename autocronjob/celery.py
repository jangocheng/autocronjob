from __future__ import absolute_import, unicode_literals
import os
from celery import Celery, platforms
import subprocess
from celery import shared_task
from time import sleep
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autocronjob.settings')

# REDIS_CONN = 'redis://%s:%d/1' % (settings.REDIS_HOST, settings.REDIS_PORT)
# app = Celery('autocronjob', backend=REDIS_CONN, broker=REDIS_CONN)
app = Celery('autocronjob')
# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
# app.config_from_object('django.conf:settings')
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# celery pool_restart bug
# 解决Celery进程重启后，正在进行中的任务丢失或者标记为失败
app.conf.update(
    worker_pool_restarts=True,
    # task_reject_on_worker_lost=True,
    # task_acks_late=True,
)

# 允许root 用户运行celery
platforms.C_FORCE_ROOT = True

from celery.utils.log import get_task_logger
import socket
logger = get_task_logger(__name__)


@app.task(bind=True)
def debug_task(self):
    # print('Request: {0!r}'.format(self.request))
    logger.info(
        '''
        task_id    : {0.id}
        task_args  : {0.args!r}
        task_kwargs: {0.kwargs!r}
        '''.format(self.request)
    )
    try:
        raise socket.error
    except socket.error as e:
        self.retry(exc=e, countdown=5, max_retries=3)
    finally:
        pass
