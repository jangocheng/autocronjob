# -*- coding:utf-8 -*-
__author__ = 'qing.cai@horizon.ai'

from django.conf import settings
import redis
from paramiko import SSHClient, AuthenticationException, RSAKey, AutoAddPolicy, SSHException


class Credential:
    def __init__(self, **kwargs):
        self.login_style = kwargs.get('login_style', None)
        self.host = kwargs.get('host', None)

    def auth(self):
        raise NotImplementedError


class SshConnect(Credential):
    def auth(self):
        try:
            if self.login_style == 'password':
                ssh = SSHClient()
                ssh.set_missing_host_key_policy(AutoAddPolicy())
                remote_port = settings.REMOTE_PORT
                if not isinstance(remote_port, int):
                    remote_port = int(remote_port)
                ssh.connect(hostname=self.host, port=remote_port, username=settings.REMOTE_USER,
                            password=settings.REMOTE_PASSWD, timeout=10)
                return {"SSH": ssh, "STATUS": True, "login_style": self.login_style}

            elif self.login_style == 'private-key':
                private_key = RSAKey.from_private_key_file(settings.PRIVATE_KEY)
                ssh = SSHClient()
                ssh.set_missing_host_key_policy(AutoAddPolicy())
                remote_port = settings.REMOTE_PORT
                if not isinstance(remote_port, int):
                    remote_port = int(remote_port)
                ssh.connect(hostname=self.host, port=remote_port, username=settings.REMOTE_USER,
                            pkey=private_key, timeout=10)
                return {"SSH": ssh, "STATUS": True, "login_style": self.login_style}

        except AuthenticationException:
            print(f'ip:{self.host} is authentication failed')
            return {"INFO": f'ip:{self.host} is authentication failed', "STATUS": False}

        except SSHException as e:
            print(f'ip:{self.host} is connection failed, Exception:{e}')
            return {"INFO": f'ip:{self.host} is connection failed', "STATUS": False}


def redis_connect(host, port, db, passwd=None):
    if passwd:
        pool = redis.ConnectionPool(host=host, port=port, password=passwd, db=db, decode_responses=True)
    else:
        pool = redis.ConnectionPool(host=host, port=port, db=db, decode_responses=True)
    r = redis.StrictRedis(connection_pool=pool)
    return r


def format_line(line):
    line = line
    if "INFO" in line:
        color = "#46A3FF"
    elif "WARN" in line:
        color = "#FFFF37"
    elif "ERROR" in line:
        color = "red"
    elif "CRITICAL" in line:
        color = "red"
    else:
        color = "#FFFFFF"

    return "<span style='color:{}'>{}</span>".format(color, line)

