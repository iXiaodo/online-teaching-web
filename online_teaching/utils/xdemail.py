# -*- coding: utf-8 -*-
#作者：xiaodong  

#创建时间：18-3-23   

#日期：下午11:48   

#：IDE：PyCharm
from tornadomail.message import EmailMessage
def send_email(self,subject='',body='',to_email=''):
    message = EmailMessage(
        subject=subject,
        body=body,
        from_email='1070457631@qq.com',
        to=[to_email],
        connection=self.mail_conn
    )
    return message
