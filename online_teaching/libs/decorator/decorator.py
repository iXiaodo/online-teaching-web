# -*- coding: utf-8 -*-
from constants import ADMIN_IP
import functools

#管理员权限通过IP地址控制，
def admin_ip_list(method):
    @functools.wraps(method)
    def wraps(self, *args, **kwargs):
        if self.request.remote_ip in ADMIN_IP:
            return method(self, *args, **kwargs)
        else:
            self.write("IP地址不在管理员列表中")
    return wraps

#另外的验证方法
def admin_auth(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.current_user:
            if self.session.get('ip_address') == self.request.remote_ip:
                return method(self, *args, **kwargs)
            else:
                self.write('ip地址不相符')
        else:
            self.write('很抱歉，用户没有登录，请登录后再试')
    return wrapper
