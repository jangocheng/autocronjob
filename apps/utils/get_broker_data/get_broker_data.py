# -*- coding:utf-8 -*-
__author__ = 'qing.cai@horizon.ai'


import redis
from django.conf import settings


def get_broker_data(queue):
    if settings.REDIS_PASSWD:
        r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                              password=settings.REDIS_PASSWD, db=settings.REDIS_DB,
                              decode_responses=True)
    else:
        r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                              db=settings.REDIS_DB, decode_responses=True)
    return r.llen(queue)
