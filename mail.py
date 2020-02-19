# An automatically send qq_email lib
# python3
# author: lunar_ubuntu
# -*- coding: UTF-8 -*-

import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.header import Header
from xml.dom.minidom import parse
import xml.dom.minidom

dom_tree = xml.dom.minidom.parse("info.xml") # here you need to fill your xml file path
elem = dom_tree.documentElement

sender = elem.getElementsByTagName("sender")[0]
sender_acount = sender.getElementsByTagName("sender_acount")[0].childNodes[0].data
sender_pwd = sender.getElementsByTagName("sender_pwd")[0].childNodes[0].data

recevs = elem.getElementsByTagName("receivers")[0]
receivers = []
for re in recevs.getElementsByTagName("receiver_acount"):
    receivers.append(re.childNodes[0].data)

def mail(*file_paths):
    res = True
    message = MIMEMultipart()
    message['From'] = Header("ubuntu",'utf-8')
    message['TO'] = Header("windows", 'utf-8')
    subject = 'ubuntu send files'
    message['Subject'] = Header(subject,'utf-8')
    for path in file_paths[0]:
        #print("path: %s" % path)
        file_name = split_path(path)
        #print("file_name: %s" % file_name)
        attach = MIMEApplication(open(path,'rb').read())
        attach['Content-type'] = 'application/octet-stream'
        attach['Content-Disposition'] = 'attachment; filename="' + file_name + '"'
        message.attach(attach)

    server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    server.login(sender_acount, sender_pwd)
    server.sendmail(sender_acount, receivers, message.as_string())
    server.quit()
    return res

def split_path(path):
    return path.split('/')[-1]

if __name__ == '__main__':
    res = mail(sys.argv[1:])
    if res:
        print("successfully send emails!")
    else:
        print("failed to send emails!")
