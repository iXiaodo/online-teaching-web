# # -*- coding: utf-8 -*-
# from tornado import web
# import json
# from libs.db.dbsession import dbSession
# from models.admin_models import CmsUsers
# from libs.pycket.session import SessionMixin
#
#
# class BaseHandler(web.RequestHandler,SessionMixin):
#
#     def initialize(self):
#         self.db = dbSession
#
#     def get_current_user(self):
#         if self.session.get("admin_name"):
#             return CmsUsers.by_name(self.session.get("admin_name"))
#         else:
#             return None
#
#     #返回结果
#     def write_response(self,response,_status=1,_err=""):
#         self.set_header('Content-type','application/json')
#         _response = {
#             "success":_status,
#             "data":response,
#             "err_msg":_err
#         }
#         self.write(json.dumps(_response))
#         self.finish()
#
#     def on_finish(self):
#         self.db.close()
#
#     #错误处理
#     def write_error(self, status_code, **kwargs):
#         if status_code==404:
#             self.render("common/404.html")
#         else:
#             self.render("common/404.html")
#
#
#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from tornado_session.sessionhandler import SessionBaseHandler
from tornado.web import HTTPError
import functools


class BaseHandler(SessionBaseHandler):
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)

    def write_response(self, response, _status=1, _err=''):
        self.set_header('Content-type', 'application/json')
        _response = {
            "success": _status,
            "data": response,
            "err_msg": _err
        }
        self.write(json.dumps(_response))
        self.finish()

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('common/404.html')
        elif status_code == 500:
            self.write('error:' + str(status_code))
        else:
            self.write('error:' + str(status_code))

    def get_current_user(self):
        # 防止安全cookies未过期 但是cookies过期的情况
        # 防止没有主动操作cookies的权力
        if self.get_session('permission') is None:
            return None
        return self.get_secure_cookie("user")

    def set_session(self, key, value):
        try:
            self.session[key] = value
            return True
        except:
            return False

    def get_session(self, key):
        try:
            return self.session[key]
        except KeyError:
            return None
        except Exception:
            return None


def is_main_account(fn):
    def wrapper(*args, **kwargs):
        if args[0].get_session("user_type") == "主账号":
            return fn(*args, **kwargs)
        else:
            args[0].write_response({}, 0, "对不起，您可能没有权限访问")
            return
    return wrapper





def permission(permission_name, permission_type):
    """
        perimission_type
        w 写
        r 读
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.get_session('raw_permission') == 'super_admin' and self.get_session('user_type') == '主账号':
                return func(self, *args, **kwargs)
            permission_dict = self.get_session('permission')
            if permission_dict is not None:
                if permission_dict.get(permission_name, {}).get(permission_type):
                    return func(self, *args, **kwargs)
                else:
                    # todo 返回无权限的界面
                    if self.request.method == 'GET':
                        self.write('<script>alert("对不起，您可能没有权限访问");history.back()</script>')
                    else:
                        self.set_header('Content-type', 'application/javascript')
                        self.write('alert("对不起，您可能没有权限访问");')
            else:
                login_url = self.get_login_url()
                self.redirect(login_url)
                return
        return wrapper
    return decorator

