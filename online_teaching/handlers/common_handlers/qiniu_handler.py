# -*- coding: utf-8 -*-
#作者：xiaodong  

#创建时间：18-1-28

#日期：下午10:55   

#：IDE：PyCharm
import qiniu.config
import json
from qiniu import Auth,put_file
from tornado.gen import coroutine
from tornado.web import authenticated
from base_handler import BaseHandler
from config import AK,SK



class get_token(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        # 1.设置accesskey和securtkey
        access_key = AK
        secret_key = SK

        # 2.授权
        q = Auth(access_key, secret_key)
        # 3.设置七牛空间
        bucket_name = 'xiaoxiao'
        # 4.生成token
        token = q.upload_token(bucket_name)
        # 5.返回token,key必须为uptoken
        #(kwargs={'uptoken': token})
        kwargs = {
            'uptoken': token
        }
        self.write_response({'uptoken': token})