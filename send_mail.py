# -*- coding: utf-8 -*-

import smtplib
import sys
import email.MIMEMultipart
import email.MIMEText
import email.MIMEBase
from email.Header import Header
import os.path
import base64

from getconf import *

#def sendmail(fullText, receivers):
def sendmail(fullText, receivers, sender, smtpaddr, user, passwd):
    print sender, receivers
    print "1", smtpaddr
    try:
        smtpObj = smtplib.SMTP(smtpaddr, 25)
        #smtpObj = smtplib.SMTP('smtp.163.com', 25)
        print "user, password", user, passwd
        smtpObj.login(user, passwd)
        #smtpObj.login('bitxyh@163.com', 68913788)
        print "2"
        try:
            smtpObj.sendmail(sender, receivers, fullText)
            print "Successfully sent mail"
        except:
            print sys.exc_info()
    except:
        print "ERROR"

#def create_attachment(data, receivers):
def create_attachment(data, text, receivers, photoname, subject, sender):
    print 'email info ', subject, sender, text, photoname

    main_msg = email.MIMEMultipart.MIMEMultipart()
    text_msg = email.MIMEText.MIMEText(text, 'plain', 'utf-8')
    main_msg.attach(text_msg)
    contype = 'application/octet-stream'
    maintype, subtype = contype.split('/', 1)

    file_msg = email.MIMEBase.MIMEBase(maintype, subtype)
    print "before decode"
    payload = base64.b64decode(data)
    print "decode over"
    file_msg.set_payload(payload)
    email.Encoders.encode_base64(file_msg)

    print photoname
    print photoname.decode('utf-8')
    file_msg.add_header('Content-Disposition','attachment', filename = photoname.decode('utf-8').encode('gb2312'))
    #file_msg.add_header('Content-Disposition','attachment', filename = photoname)
    main_msg.attach(file_msg)
    main_msg['From'] = sender
    main_msg['To'] = receivers
    main_msg['Subject'] = Header(subject, 'utf-8')
    main_msg['Date'] = email.Utils.formatdate()

    fullText = main_msg.as_string()
    print "fulltext ok"
    return fullText



if __name__ == "__main__":
        sender = get_mail_config('email_info', 'sender')
        smtpaddr = get_mail_config('email_info', 'smtpserver')
        username = get_mail_config('email_info', 'username')
        passwd = get_mail_config('email_info', 'passwd')
        subject = get_mail_config('email_info', 'subject')
        text = get_mail_config('email_info', 'text')
        photoname = get_mail_config('email_info', 'photoname')
        #photoname = photo.decode('utf-8')

        receivers = 'zhangpp@9stars.cn'
        data = base64.b64encode("000")
        fullText = create_attachment(data, text, receivers, photoname, subject, sender)
        print "ready to send"
        sendmail(fullText, receivers, sender, smtpaddr, username, passwd)
        print "send photo over.OK"
