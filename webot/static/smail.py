#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
当采集数据不符合固定伐值要求时，send mail
2014/01/26 www
"""

#导入smtplib和MIMEText
import smtplib
from email.mime.text import MIMEText

def send_mail(to_list,sub,content):
    #设置服务器，用户名、口令以及邮箱的后缀
    mail_host="smtp.exmail.qq.com:465"
    mail_user="alert"
    mail_pass="yqzb_140101"
    mail_postfix="yqzbw.com"
    me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content)
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = to_list
    try:
        s = smtplib.SMTP_SSL()
        s.connect(mail_host)
        s.ehlo('hello')
        s.login(mail_user+'@'+mail_postfix,mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False
if __name__ == '__main__':
    if send_mail('wangweiwei@yqzbw.com',"hi","nice to meet you !!!"):
        print "发送成功"
    else:
        print "发送失败"
