# -*- coding:utf-8 -*-
__author__ = 'qing.cai@horizon.ai'

import urllib
from http import cookiejar
import urllib.request
import urllib.parse
import re


def get_cookie(login_url, name, passwd):
    auth_url = login_url
    # 登陆用户名和密码
    data = {
        "name": name,
        "password": passwd
    }
    # urllib进行编码
    post_data = urllib.parse.urlencode(data)
    # 发送头信息
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json, text/plain, */*"
    }
    # 初始化一个CookieJar来处理Cookie
    # cookieJar = cookielib.CookieJar()
    # 实例化一个全局opener
    # opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
    req = urllib.request.Request(auth_url, post_data, headers)
    req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')
    # 拼接成cookie file
    filename = "%s.txt" % ('_'.join(login_url.split('/')[2].split('.')))
    ckjar = cookiejar.MozillaCookieJar(filename)
    ckproc = urllib.request.HTTPCookieProcessor(ckjar)
    opener = urllib.request.build_opener(ckproc)
    f = opener.open(req)
    htm = f.read()
    f.close()
    ckjar.save(ignore_discard=True, ignore_expires=True)
