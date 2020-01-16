# -*- coding:utf-8 -*-
__author__ = 'qing.cai@horizon.ai'

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import os
channel_layer = get_channel_layer()
import time


def to_ws_message(step, send_data, file_name):
    '''
    发送给websocket数据
    :param step:
    :param send_data:
    :return:
    '''
    time.sleep(0.5)
    async_to_sync(channel_layer.group_send)(
        'dag_'+str(os.path.basename(file_name).split('.py')[0]),
        {
            "type": "send.message",
            "message": {"step": "%s" % step, "msg": "%s" % send_data}
        }
    )

