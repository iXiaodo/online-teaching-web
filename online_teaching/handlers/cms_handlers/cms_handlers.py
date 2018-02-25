# -*- coding: utf-8 -*-

from handlers.common_handlers.base_handler import BaseHandler
from models.admin_models import CmsUsers
from datetime import datetime
from libs.decorator.decorator import admin_ip_list,admin_auth
#首页

#登录处理
login_add = 0
class CmsLoginHandler(BaseHandler):
    @admin_ip_list
    def get(self):
        self.render("cms/cms_login.html")

    def post(self):
        global login_add
        email = self.get_argument('email', '')
        if email:
            admin = CmsUsers.by_email(email)
        password = self.get_argument("password", "")
        if login_add <= 3:
            if not admin._locked:
                if admin and admin.auth_password(password):
                    self.success_login(admin)
                    self.redirect("/cms/")
                else:
                    login_add += 1
                    self.redirect('/cms/login/')
            else:
                self.write("用户由于非法操作超过3次，已被锁,请联系管理员！")

        else:
            admin.locked = True
            # self.db.add(admin)
            self.db.commit()
            self.write("对不起，密码输入连续错误3次！用户已被锁，请联系管理员！")


    def success_login(self, admin):
        admin.last_login = datetime.now()
        admin.loginnum += 1
        self.db.add(admin)
        self.db.commit()
        self.session.set('admin_name', admin.username)
        self.session.set('ip_address',self.request.remote_ip)

class CmsIndexHandler(BaseHandler):
    @admin_ip_list
    @admin_auth
    def get(self):
        self.render("cms/cms_index.html")




