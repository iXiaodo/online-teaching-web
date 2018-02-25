# -*- coding: utf-8 -*-
from tornado import web
import json
from libs.db.dbsession import dbSession
from models.admin_models import CmsUsers
from libs.pycket.session import SessionMixin


class BaseHandler(web.RequestHandler,SessionMixin):

    def initialize(self):
        self.db = dbSession

    def get_current_user(self):
        if self.session.get("admin_name"):
            return CmsUsers.by_name(self.session.get("admin_name"))
        else:
            return None


    def get(self,**kwargs):
        pass

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

    def on_finish(self):
        self.db.close()

    #错误处理
    def write_error(self, status_code, **kwargs):
        if status_code==404:
            self.render("common/404.html")
        else:
            self.render("common/404.html")


