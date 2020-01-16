# -*- coding:utf-8 -*-

__author__ = 'qing.cai@horizon.ai'


import smtplib

import os
from email.mime.text import MIMEText
from autocronjob.settings import BASE_DIR
import configparser


config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, 'autocronjob.conf'))
mail_user = config.get('mail', 'mail_user')
mail_pass = config.get('mail', 'mail_pass')
smtp_server = config.get('mail', 'smtp_server')


def sendmail(mailto, subject, body, format='plain', Cc=None):
    if isinstance(body, str):
        body = str(body)

    msg = MIMEText(body, _subtype='html', _charset='utf-8')
    if not isinstance(subject, str):
        subject = str(subject)
    msg['Subject'] = subject
    msg['From'] = "sms@horizon-robotics.com"
    msg['To'] = mailto
    msg["Accept-Language"] = "zh-CN"
    msg["Accept-Charset"] = "ISO-8859-1,utf-8"
    msg["Cc"] = Cc
    try:
        s = smtplib.SMTP()
        s.connect("smtp.exmail.qq.com")
        s.login("sms@horizon-robotics.com", "12162828SmS")
        s.send_message(msg, from_addr="sms@horizon-robotics.com")
        s.close()
        return True
    except Exception as e:
        print(str(e))
        return False
