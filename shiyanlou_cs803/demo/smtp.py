#!/usr/bin/env python
#coding: utf8

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from subprocess import check_output

receiver = 'receiver@qq.com'
mail_host = 'smtp.qq.com'
mail_user = 'yourname@qq.com'
mail_pass = 'yourpasscode'

sender = mail_user
receivers = [receiver]

message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
message['From'] = Header(mail_user, 'utf-8')
message['To'] = Header(str(receivers), 'utf-8')

subject = 'my test'
message['Subject'] = Header(subject, 'utf-8')

try:
    smtpObj = smtplib.SMTP_SSL(mail_host, 465)
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    smtpObj.quit()
    print("邮件发送成功！")
except smtplib.SMTPException as e:
    print(e)
