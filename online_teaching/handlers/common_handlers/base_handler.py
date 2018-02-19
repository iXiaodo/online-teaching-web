# -*- coding: utf-8 -*-
from tornado import web
import json



class BaseHandler(web.RequestHandler):

    #返回结果
    def write_response(self,response,_status=1,_err=""):
        self.set_header('Content-type','application/json')
        _response = {
            "success":_status,
            "data":response,
            "err_msg":_err
        }
        self.write(json.dumps(_response))
        self.finish()

    #错误处理
    def write_error(self, status_code, **kwargs):
        if status_code==404:
            self.render("common/404.html")
        else:
            self.render("common/404.html")