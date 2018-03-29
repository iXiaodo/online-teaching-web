# -*- coding: utf-8 -*-
from tornado.gen import Return, coroutine
from tornado.web import authenticated
from geetest import GeetestLib
from handlers.common_handlers.base_handler import BaseHandler
from config import GT_KEY, GT_ID, MongoBasicInfoDb, CMS_USER

from utils.hashers import make_password
from libs.motor.base import BaseMotor
from log import *
from models.cms_user import CmsUser



#首页
class IndexHandler(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        try:
            email = self.get_session("current_email")
            args = {
                "title": "后台管理系统",
                "role": self.get_session("role"),
                "email": email,
                "permission": self.get_session("permission")
            }
            self.render("cms/base.html", **args)
        except Exception as e:
            logging.exception(e)
            self.write_response({},0,_err=e)

#用户信息页面
class CmsProfilePageHandler(BaseHandler):
    @coroutine
    @authenticated
    def get(self):
        try:
            email = self.get_session("current_email")
            args = {
                "title": "后台管理系统",
                "role": self.get_session("role"),
                "email": email,
                "permission": self.get_session("permission")
            }
            user_coll = BaseMotor().client[MongoBasicInfoDb][CMS_USER]
            user_doc = yield user_coll.find_one({"_id": email})
            args['user_name']=user_doc['user_name']
            args['user_email']=user_doc['user_email']
            args['tel']=user_doc['tel']
            args['status']=str(user_doc['status'])
            self.render("cms/cms_profile.html",**args)
        except Exception as e:
            logging.exception(e)

#管理员登录处理
class CmsLoginHandler(BaseHandler):
    @coroutine
    def get(self):
        next_url = self.get_argument('next', '/cms/')
        self.set_cookie('_xsrf',self.xsrf_token)
        msg = ''
        if next_url == '/cms/logout':
            next_url = '/cms/'
        self.render("cms/user_login.html",msg = msg,next_url=next_url)

    @coroutine
    def post(self):
        next_url = self.get_argument('next', '/cms/')
        try:
            gt = GeetestLib(GT_ID, GT_KEY)
            challenge = self.get_argument(gt.FN_CHALLENGE, "")
            validate = self.get_argument(gt.FN_VALIDATE, "")
            seccode = self.get_argument(gt.FN_SECCODE, "")
            status = int(self.session[gt.GT_STATUS_SESSION_KEY])
            user_id = self.session["user_id"]
            password = self.get_argument('password')
            password = make_password(password)
            if status:
                verify_res = gt.success_validate(challenge, validate, seccode, user_id)
            else:
                verify_res = gt.failback_validate(challenge, validate, seccode)
                self.session["user_id"] = user_id
            if verify_res:
                try:
                    user_email = self.get_argument('user_email')
                    cms_user_coll = BaseMotor().client[MongoBasicInfoDb][CMS_USER]
                    cms_user_doc = yield cms_user_coll.find_one({"_id":user_email})
                    if not cms_user_doc:
                        self.render("cms/user_login.html", msg="账户不存在", next_url=next_url)
                    else:
                        pwd = cms_user_doc['password']
                        if pwd == password:
                            self.session['current_email'] = user_email
                            self.session['role'] = cms_user_doc['role']
                            self.session['permission'] = cms_user_doc['permission']
                            self.set_secure_cookie("user", user_email + cms_user_doc['role'],expires_days=1)
                            self.redirect(next_url)
                        else:
                            msg = "此账号密码有误,请重新输入！"
                            self.render("cms/user_login.html", msg=msg, next_url=next_url)
                except Exception as e:
                    logging.exception(e)
                    msg = "账户出现异常！"
                    self.render("cms/user_login.html", msg=msg, next_url=next_url)
            else:
                msg = '验证码验证失败，请重新验证'
                self.render("cms/user_login.html", msg=msg, next_url=next_url)
        except Exception as e:
            logging.exception(e)
            msg = '验证码参数获取异常，请稍后重试'
            self.render("cms/user_login.html", msg=msg, next_url=next_url)



class CmsLogoutHandler(BaseHandler):
    # 权限认证
    @coroutine
    def get(self, *args, **kwargs):
        self.clear_all_cookies()
        msg = '安全退出成功，请重新登录'
        self.render("cms/user_login.html", msg=msg, next_url='/cms/')









class CmsModifyPwdHandler(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        email = self.get_session("current_email")
        args = {
            "title": "修改当前账户密码",
            "role": self.get_session("role"),
            "email": email,
            "permission": self.get_session("permission")
        }
        self.render("cms/cms_modifyPwd.html",**args)


    def post(self):
        pass

#版本信息
class CmsVersionHandler(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        try:
            email = self.get_session("current_email")
            args = {
                "title": "版本信息",
                "role": self.get_session("role"),
                "email": email,
                "permission": self.get_session("permission")
            }
            self.render("cms/cms_version.html", **args)
        except Exception as e:
            logging.exception(e)
            self.write_response({},0,_err=e)


#账户管理
class CmsSubAccountHandler(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        email = self.get_session("current_email")
        args = {
            "title": "子账户管理",
            "role": self.get_session("role"),
            "email": email,
            "permission": self.get_session("permission")
        }
        self.render("cms/cms_subAccount.html",**args)



class CmsDataManageHandler(BaseHandler):
    def get(self):
        email = self.get_session("current_email")
        args = {
            "title": "资料管理",
            "role": self.get_session("role"),
            "email": email,
            "permission": self.get_session("permission")
        }
        self.render("cms/file_up.html",**args)



