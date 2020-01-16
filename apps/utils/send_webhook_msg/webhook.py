# -*- coding:utf-8 -*-
__author__ = 'qing.cai@horizon.ai'

import requests
import json

headers = {'Content-Type': 'application/json;charset=utf-8'}


def send_webhook(url, text):
    json_text = {
        "msgtype": "markdown",
        "markdown": {
           "content": "AutoCronjob<font color=\"warning\">告警</font>,请及时查看。\n>告警详情:"+text
        }
    }
    return requests.post(url, json.dumps(json_text), headers=headers).content
