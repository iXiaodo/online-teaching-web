# -*- coding: utf-8 -*-
from handlers.common_handlers.base_handler import BaseHandler

#首页
class IndexHandler(BaseHandler):
    def get(self):
        self.render("front/front_base.html")

#----------------------------------------------------------登录
class SignInHandler(BaseHandler):
    def get(self):
        self.render("front/front_signin.html")


#----------------------------------------------------------注册
class SignUpHandler(BaseHandler):
    def get(self):
        self.render("front/front_signup.html")


#----------------------------------------------------------忘记密码
class ForgetPwdHandler(BaseHandler):

    def get(self,error='',info=''):
        context = {
            'error':error,
            'info':info
        }
        self.render("front/front_forgetpwd.html",**context)