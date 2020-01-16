# -*- coding:utf-8 -*-
from __future__ import unicode_literals, division


import math
import time
import sys
import socket
import signal
import redis
import os

FLAG = True


def redis_connect(host, port, db, passwd=None):
    if passwd:
        pool = redis.ConnectionPool(host=host, port=port, password=passwd, db=db, decode_responses=True)
    else:
        pool = redis.ConnectionPool(host=host, port=port, db=db, decode_responses=True)
    r = redis.StrictRedis(connection_pool=pool)
    return r


def get_last_lines(f, num=10):
    """读取文件的最后几行
    """
    size = 1000
    try:
        f.seek(-size, 2)
    except IOError:  # 文件内容不足size
        f.seek(0)
        return f.readlines()[-num:]

    data = f.read()
    lines = data.splitlines()
    n = len(lines)
    while n < num:
        size *= int(math.ceil(num / n))
        try:
            f.seek(-size, 2)
        except IOError:
            f.seek(0)
            return f.readlines()[-num:]
        data = f.read()
        lines = data.splitlines()
        n = len(lines)

    return lines[-num:]


def process_line(r, channel, line):
    r.publish(channel, line.strip())


def sig_handler(signum, frame):
    global FLAG
    FLAG = False


# 收到退出信号后，以比较优雅的方式终止脚本
signal.signal(signal.SIGTERM, sig_handler)
# 为了避免日志输出过多，浏览器承受不住，设置10分钟后脚本自动停止
signal.signal(signal.SIGALRM, sig_handler)
signal.alarm(600)


def get_hostname():
    return socket.gethostname()


def force_str(s):
    if isinstance(s, str):
        s = s.encode("utf-8")
    return s


def tail():
    """
    1: redis host
    2: redis port
    3: redis db
    4: hostname
    5: logfile
    6: line
    7: redis passwd
    """
    if sys.argv[7]:
        r = redis_connect(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[7])
    else:
        r = redis_connect(sys.argv[1], sys.argv[2], sys.argv[3])
    line_count = int(sys.argv[6])
    # 往redis频道发送实时日志
    channel = "logs:{hostname}".format(hostname=sys.argv[4])

    with open(sys.argv[5], 'r') as f:
        last_lines = get_last_lines(f, line_count)
        for line in last_lines:
            process_line(r, channel, force_str(line))
        try:
            while FLAG:  # 通过信号控制这个变量，实现优雅退出循环
                line = f.readline()
                if not line:
                    time.sleep(0.05)
                    continue
                process_line(r, channel, line)
        except KeyboardInterrupt:
            pass
    print("Exiting...")


if __name__ == "__main__":
    if len(sys.argv) < 7:
        print("Args error")
        exit(1)
    tail()
