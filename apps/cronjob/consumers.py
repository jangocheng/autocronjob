import json
import os
import datetime
import urllib.parse
from channels.generic.websocket import \
    WebsocketConsumer, AsyncWebsocketConsumer, SyncConsumer
from apps.utils.remote_tailf_logfile.ssh_connect import \
    SshConnect, redis_connect
from django.conf import settings

from asgiref.sync import async_to_sync
from cronjob.tasks import remote_tailf_log, local_tailf_log


class DagStatusConsumer(WebsocketConsumer):

    def connect(self):
        self.daggroup_name = urllib.parse.unquote(
            self.scope['query_string'].decode("utf-8")).split('=')[1]
        async_to_sync(self.channel_layer.group_add)(
            self.daggroup_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.daggroup_name,
            self.channel_name
        )

    def send_message(self, event):
        self.send(text_data=json.dumps({
            "message": event["message"]
        }))


class RemoteTailfLogConsumer(WebsocketConsumer):
    """
    查看实时远程调度日志
    """

    def connect(self):
        self.hostname = self.scope["url_route"]["kwargs"]["hostname"]
        if settings.REMOTE_PASSWD:
            login_style = 'password'
        else:
            login_style = 'private-key'
        self.ssh = SshConnect(**{
            "host": f"{self.hostname}",
            "login_style": login_style
        }).auth()
        if self.ssh['STATUS']:
            print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
                  f' INFO] {self.hostname} ssh connect success'
                  )
            self.ssh_obj = self.ssh['SSH']
            # 异步执行命令
            script_file = os.path.join(
                settings.BASE_DIR, 'apps/utils/remote_tailf_logfile/'
                                   'nohup_exec_cmd.sh')
            line = 10
            stdin, stdout, stderr = self.ssh_obj.exec_command(
                f"sh {script_file} {settings.REDIS_HOST} {settings.REDIS_PORT}"
                f" {settings.LOG_DB} {self.hostname} {settings.LOG_FILE} "
                f"{line} {settings.REDIS_PASSWD}"
            )
            self.key = f"logs:{self.hostname}"
            print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
                  f' INFO] {self.hostname} ssh connect closed'
                  )
            self.ssh_obj.close()
            print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
                  f' INFO] {self.hostname} websocket success'
                  )
        else:
            print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
                  f' ERROR] {self.hostname} ssh connect failed'
                  )
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        if self.ssh['STATUS']:
            self.result = remote_tailf_log.delay(**{
                "channel_name": self.channel_name,
                "key": self.key
            })
            print(
                f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
                f' INFO] {json.loads(text_data)["INFO"]}, connect:',
                self.channel_name, self.result.id
            )
        else:
            async_to_sync(self.channel_layer.send)(
                self.channel_name,
                {
                    "type": "send.message",
                    "message": self.ssh['INFO']
                }
            )

    def disconnect(self, close_code):
        if self.ssh['STATUS']:
            self.result.revoke(terminate=True)
        print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} INFO]'
              f' {self.hostname} websocket closed'
              )

    def send_message(self, event):
        self.send(text_data=json.dumps({
            "message": event["message"]
        }))


class LocalTailfLogConsumer(AsyncWebsocketConsumer):
    """
    查看实时本地调度日志
    """

    async def connect(self):
        self.hostname = self.scope["url_route"]["kwargs"]["hostname"]
        logfile = settings.LOG_FILE
        self.result = local_tailf_log.delay(**{
            "channel_name": self.channel_name,
            "logfile": logfile, "line_count": 10
        })
        print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} INFO]'
              f' {self.hostname} websocket success'
              )
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        print(
            f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} INFO]'
            f' {json.loads(text_data)["INFO"]}, connect:',
            self.channel_name, self.result.id
        )

    async def disconnect(self, close_code):
        # 中止执行中的Task
        self.result.revoke(terminate=True)
        print(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} INFO]'
              f' {self.hostname} websocket closed'
              )

    async def send_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))
