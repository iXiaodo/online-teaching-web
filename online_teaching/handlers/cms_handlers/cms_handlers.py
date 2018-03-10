# -*- coding: utf-8 -*-

from handlers.common_handlers.base_handler import BaseHandler
from models.admin_models import CmsUsers
from datetime import datetime
from libs.decorator.decorator import admin_ip_list,admin_auth
from tornado.gen import Return, coroutine
from tornado.web import authenticated
from config import GT_KEY, GT_ID,PERMISSION_NAME_COLLECTION,MongoBasicInfoDb
# from config import BaseMongodbDb
# from database.motor.base import BaseMotor
from geetest import GeetestLib
from config import permission_list
from libs.decorator.decorator import permission
from models.account import Account,AccountNotExistError
import json
from utils.hashers import make_password
from libs.motor.base import BaseMotor
from log import *

#首页
class IndexHandler(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        args = {
            "title": "后台管理系统",
            "user_type": self.get_session("user_type"),
            "username": self.get_session("main_account_email") + "::" + self.get_session(
                "sub_account") if self.get_session("sub_account") else self.get_session("main_account_email"),
            "subAccount": True if self.get_session('user_type') == '主账号' else
            self.get_session('permission').get('subAccountManage'),
            "permission": permission_list if self.get_session('user_type') == '主账号' else get_page_permission(
                self.get_session('permission'))
        }
        self.render("cms/base.html", **args)

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
            if status:
                verify_res = gt.success_validate(challenge, validate, seccode, user_id)
            else:
                verify_res = gt.failback_validate(challenge, validate, seccode)
                self.session["user_id"] = user_id
            if verify_res:
                user_email = self.get_argument('user_email')
                try:
                    subaccount_id = self.get_argument('sub_account')
                    if subaccount_id == '':
                        subaccount_id = None
                except:
                    subaccount_id = None
                password = self.get_argument('password')
                password = make_password(password)
                try:
                    account = Account(user_email, subaccount_id)
                    main_account = Account(user_email)
                except AccountNotExistError:
                    self.clear_session_obj()
                    msg = "账户不存在,请重新输入"
                    self.render("cms/user_login.html", msg=msg, next_url=next_url)
                    return
                except Exception:
                    msg = "账户出现异常！"
                    self.render("cms/user_login.html", msg=msg, next_url=next_url)
                    return
                if account.document.get("password") == password:
                    if account.is_main_account and account.document.get("permission") == "super_admin":
                        permision = {'status': True}
                    else:
                        permision = yield self.getPermission(user_email, subaccount_id)
                    if permision['status']:
                        self.session['raw_permission'] = account.document.get("permission")
                        self.session['user_type'] = '主账号' if account.is_main_account else '子账号'
                        self.session['user_name'] = account.document.get("user_name")
                        self.session['permission'] = permision
                        self.session['version'] = main_account.document.get("product_version")
                        self.session['sub_account'] = subaccount_id
                        self.session["role"] = account.role
                        self.session["group"] = account.group
                        self.session['main_account_email'] = user_email
                        self.set_secure_cookie("user", user_email + subaccount_id if subaccount_id else user_email,
                                               expires_days=1)
                        self.redirect(next_url)
                        return
                    else:
                        self.clear_session_obj()
                        msg = '获取权限分组异常'
                        self.render("cms/user_login.html", msg=msg, next_url=next_url)
                        return
                else:
                    self.clear_session_obj()
                    msg = "账号密码错误,请重新输入！"
                    self.render("cms/user_login.html", msg=msg, next_url=next_url)
            else:
                self.clear_session_obj()
                msg = '验证码验证失败，请重新验证'
                self.render("cms/user_login.html", msg=msg, next_url=next_url)
        except Exception:
            msg = '登录出现异常，请稍后重试'
            self.render("cms/user_login.html", msg=msg, next_url=next_url)

    @coroutine
    def getPermission(self, main_account, subaccount_id):
        collection = BaseMotor().client[MongoBasicInfoDb][PERMISSION_NAME_COLLECTION]
        result = yield collection.find_one({'_id': str(main_account)})
        if result is None:
            raise Return({'status': False, 'err_msg': '账号不存在'})
        if result.get(subaccount_id):
            result[subaccount_id]['status'] = True
            raise Return(result[subaccount_id])
        else:
            raise Return({"status": False})


class CmsLogoutHandler(BaseHandler):
    # 登陆认证
    @authenticated
    # 权限认证
    @coroutine
    def get(self, *args, **kwargs):
        user_id = self.get_session()
        self.clear_session_obj(user_id)
        self.clear_all_cookies()
        msg = '安全退出成功，请重新登录'
        self.render("cms/user_login.html", msg=msg, next_url='/cms/')


# 验证码处理
class PcGetCaptchaHandler(BaseHandler):
    @coroutine
    def get(self):
        user_id = 'test'
        try:
            gt = GeetestLib(GT_ID, GT_KEY)
            status = gt.pre_process(user_id)
            self.session[gt.GT_STATUS_SESSION_KEY] = str(status)
            self.session["user_id"] = user_id
            response_str = gt.get_response_str()
            self.write(response_str)
        except Exception as e:
            # logging.exception(e)
            self.write('对不起，请求验证码异常')






class CmsModifyPwdHandler(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        self.render("cms/cms_modifyPwd.html",title="修改账户密码")


#版本信息
class CmsVersionHandler(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        self.render("cms/cms_version.html",title="版本信息")




#子账户管理
class CmsSubAccountHandler(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        self.render("cms/cms_subAccount.html",title="子账户管理")



