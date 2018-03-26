# coding: utf-8
import functools
import json
import logging
from tornado_session.sessionhandler import SessionBaseHandler
from tornadomail.message import EmailFromTemplate   # 导入EmailFromTemplate
from tornadomail.backends.smtp import EmailBackend
from tornado import template,web

from libs.redis.redis_conn import conn



class BaseHandler(SessionBaseHandler):
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)

    def initialize(self):
        self.conn = conn

    @property
    def mail_connection(self):
        return EmailBackend(
            'smtp.qq.com', 587, '1070457631@qq.com','ayzumyiiervqbdig', 'WABC_940522',
            True
        )

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


    #email 配置
    @property
    def mail_conn(self):
        return self.mail_connection


def is_main_account(fn):
    def wrapper(*args, **kwargs):
        if args[0].get_session("user_type") == "超级管理员":
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
            if self.get_session('raw_permission') == 'super_admin' and self.get_session('user_type') == '超级管理员':
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

