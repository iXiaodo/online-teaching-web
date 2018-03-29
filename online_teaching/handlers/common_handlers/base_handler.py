# coding: utf-8
import json
from tornado_session.sessionhandler import SessionBaseHandler
from tornadomail.backends.smtp import EmailBackend
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

    def write_response(self, response, _status=1, _err='',kwargs={}):
        self.set_header('Content-type', 'application/json')
        _response = {
            "success": _status,
            "data": response,
            "err_msg": _err
        }
        if kwargs:
            for k,v in kwargs.items():
                _response[k] = v
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




