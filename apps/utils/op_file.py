# -*- coding:utf-8 -*-
__author__ = 'qing.cai@horizon.ai'


import math


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