# -*- coding: utf-8 -*-

from celery import Celery

import sys
sys.path.append("..")
from send_mail import sendmail, create_attachment

CELERY_BROKER_URL='redis://localhost:6379',
CELERY_RESULT_BACKEND='redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['json']

celery = Celery('tasks', backend=CELERY_RESULT_BACKEND, broker=CELERY_BROKER_URL)
celery.conf.CELERY_TASK_SERIALIZER = 'json'


@celery.task()
def send_comment_mail(para_dic):
    print "send photo start."
    print para_dic
    #fullText = create_attachment(data, receivers)
    fullText = create_attachment(para_dic['data'], para_dic['text'], para_dic['receivers'], para_dic['photoname'], para_dic['subject'], para_dic['sender'])
    #sendmail(fullText, receivers)
    sendmail(fullText, para_dic['receivers'], para_dic['sender'], para_dic['smtpaddr'], para_dic['username'], para_dic['passwd'])
    print "send photo over.OK"

