# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals
__author__ = 'qing.cai@horizon.ai'

from celery import shared_task, exceptions
from django_celery_beat.models import PeriodicTask, MailAddress, WebhookUrl
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from utils.send_mail import content, send_mail
from utils.send_webhook_msg.webhook import send_webhook
from time import sleep
import subprocess
import datetime
import json
import shlex
import time

from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from apps.utils.remote_tailf_logfile.ssh_connect import redis_connect, format_line
from apps.utils.op_file import get_last_lines

r = redis_connect(settings.REDIS_HOST, settings.REDIS_PORT, settings.LOG_DB, settings.REDIS_PASSWD)
channel_layer = get_channel_layer()
logfile = settings.LOG_FILE


@shared_task
def runs_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True)
    stdout = ''
    try:
        # Read stdout from subprocess until the buffer is empty !
        for line in iter(p.stdout.readline, b''):
            if line:  # Don't print blank lines
                # linedata = ','.join([str(stdout, encoding="utf-8").strip() for stdout in line])
                # linedata += stdout
                stdout += str(line, encoding="utf-8")
            else:
                 stdout = 'normal running'
        # This ensures the process has completed, AND sets the 'returncode' attr
        while p.poll() is None:
            sleep(.1)  # Don't waste CPU-cycles
        # Empty STDERR buffer
        err = p.stderr.read()
        if p.returncode == 0:
            """
            运行指令成功，返回指令运行结果/运行正常消息
            """
            return stdout
        else:
            """
            运行指令失败，发送邮件/webhook消息
            """
            try:
                result_data = {"datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                               "info": str(err, encoding="utf-8")}
                cronjob_obj = PeriodicTask.objects.get(Q(kwargs__contains="%s" % command) | Q(args__contains="%s" % command))
            except ObjectDoesNotExist as e:
                exceptions_data = {"datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                               "info": e}

                send_mail.sendmail(mailto="%s" % "qing.cai@horizon.ai", subject="AutoCronjob告警",
                                   body=content.msg(command, json.dumps(exceptions_data, indent=4)))
                return 'task exec error, send mail abnormal!'

            if cronjob_obj.mail_monitor_enabled:
                mailaddress = MailAddress.objects.get(id=cronjob_obj.mailaddress_id).mailaddress
                send_mail.sendmail(mailto="%s" % str(mailaddress), subject="AutoCronjob告警",
                                   body=content.msg(command, json.dumps(result_data, indent=4)))
            if cronjob_obj.webhook_monitor_enabled:
                webhookurl = WebhookUrl.objects.get(id=cronjob_obj.webhookurl_id).webhookurl
                send_webhook("%s" % webhookurl, "%s" % result_data)

            # The runs_command() function is responsible for logging STDERR
            return "Error traceback: " + str(err, encoding="utf-8")

    # Manually running the view has the configuration
    except exceptions.SoftTimeLimitExceeded:
        return 'stdout', 'exec timeout'


@shared_task(ignore_result=True)
def remote_tailf_log(**kwargs):
    channel_name = kwargs.get('channel_name', None)
    key = kwargs.get('key', None)
    channel = r.pubsub()
    channel.subscribe(key)
    try:
        for item in channel.listen():
            if item['type'] == 'message':
                line = format_line(item['data'])
                async_to_sync(channel_layer.send)(
                    channel_name,
                    {
                        "type": "send.message",
                        "message": line
                    }
                )
            if item['data'] == 'over':
                break
    except Exception as e:
        print(e)
    print('exec unsubscribe')
    channel.unsubscribe(key)


@shared_task(ignore_result=True)
def local_tailf_log(**kwargs):
    channel_name = kwargs.get('channel_name', None)
    line_count = kwargs.get('line_count', None)
    logfile = kwargs.get('logfile', None)
    try:
        with open(logfile) as f:
            f.seek(0, 2)
            last_lines = get_last_lines(f, line_count)
            for line in last_lines:
                async_to_sync(channel_layer.send)(
                    channel_name,
                    {
                        "type": "send.message",
                        "message": format_line(line)
                    }
                )
            while True:
                line = f.readline()
                if line:
                    line = format_line(line)
                    async_to_sync(channel_layer.send)(
                        channel_name,
                        {
                            "type": "send.message",
                            "message": line
                        }
                    )
                else:
                    time.sleep(0.5)
    except Exception as e:
        print(e)
