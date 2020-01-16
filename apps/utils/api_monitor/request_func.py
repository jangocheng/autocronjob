# -*- coding:utf-8 -*-
__author__ = 'qing.cai@horizon.ai'


import urllib.request
from http import cookiejar
import json


def api_func(api_url):
    url = "http://biaozhu.horizon.ai/datasys/rbac/user/info/"
    header = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    request = urllib.request.Request(url, headers=header)

    cookie = cookiejar.MozillaCookieJar()
    filename = "%s.txt" % ('_'.join(api_url.split('/')[2].split('.')))
    cookie.load(filename)

    cookie_handler = urllib.request.HTTPCookieProcessor(cookie)
    cookie_opener = urllib.request.build_opener(cookie_handler)

    response = cookie_opener.open(request)
    responses = json.loads(response.read())
    response.close()
    print(responses)

