# -*- coding: utf-8 -*-
import logging
from handlers.common_handlers.base_handler import BaseHandler
from tornado.gen import Return, coroutine
from tornado.web import authenticated
from config import GT_KEY, GT_ID,PERMISSION_NAME_COLLECTION,MongoBasicInfoDb,USER_NAME_COLLECTION
from geetest import GeetestLib
from pages.handlers import permission_list, get_page_permission
from models.account import Account,AccountNotExistError
from utils.hashers import make_password
from libs.motor.base import BaseMotor


#首页
class IndexHandler(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        email = self.get_session("main_account_email")
        args = {
            "title": "后台管理系统",
            "user_type": self.get_session("user_type"),
            "email": email,
            "permission": permission_list if self.get_session('user_type') == '超级管理员' else get_page_permission(
                self.get_session('permission'))
        }
        try:
            email = self.get_session("subaccount_email")
            if email:
                args["email"]=email
            print args['permission']
            self.render("cms/base.html", **args)
        except Exception as e:
            print e
            logging.exception(e)
            self.write_response({},0,_err=e)

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
            print verify_res
            if verify_res:
                try:
                    user_email = self.get_argument('user_email')
                    subaccount_id = self.get_argument('sub_account')
                    if subaccount_id == '':
                        subaccount_id = None
                    account = Account(user_email, subaccount_id)
                    main_account = Account(user_email)
                except AccountNotExistError as e:
                    logging.exception(e)
                    msg = "账户不存在,请重新输入"
                    self.render("cms/user_login.html", msg=msg, next_url=next_url)
                    return
                except Exception as e:
                    logging.exception(e)
                    print e
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
                        self.session['user_type'] = '超级管理员' if account.is_main_account else account.role
                        self.session['user_name'] = account.document.get("user_name")
                        self.session['permission'] = permision
                        self.session['sub_account'] = subaccount_id
                        self.session["role"] = account.role
                        self.session["group"] = account.group
                        self.session['main_account_email'] = user_email
                        if subaccount_id:
                            coll = BaseMotor().client[MongoBasicInfoDb][USER_NAME_COLLECTION]
                            res = yield coll.find_one({'_id': user_email})
                            email = res["subaccount"][subaccount_id]["user_email"]
                            self.session['subaccount_email']=email
                        self.set_secure_cookie("user", user_email + subaccount_id if subaccount_id else user_email,
                                               expires_days=1)
                        self.redirect(next_url)
                        return
                    else:
                        msg = '获取权限分组异常'
                        self.render("cms/user_login.html", msg=msg, next_url=next_url)
                        return
                else:
                    msg = "此账号密码有误,请重新输入！"
                    self.render("cms/user_login.html", msg=msg, next_url=next_url)
            else:
                msg = '验证码验证失败，请重新验证'
                self.render("cms/user_login.html", msg=msg, next_url=next_url)
        except Exception as e:
            logging.exception(e)
            msg = '验证码参数获取异常，请稍后重试'
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
    # 权限认证
    @coroutine
    def get(self, *args, **kwargs):
        # user_id = self.get_session('user_id')
        # self.clear_session_obj(user_id)
        self.clear_all_cookies()
        msg = '安全退出成功，请重新登录'
        self.render("cms/user_login.html", msg=msg, next_url='/cms/')









class CmsModifyPwdHandler(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        args = {
            'user_type': self.session.get('user_type'),
            'username':self.session.get('user_name'),
            'title':"修改账户密码"
        }
        self.render("cms/cms_modifyPwd.html",**args)


#版本信息
class CmsVersionHandler(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        user_type = self.session.get('user_type')
        email = self.get_session("main_account_email")
        account_email = self.get_session("subaccount_email")
        args = {
            'user_type':user_type,
            'title':'版本信息',
            'email':email,
            "permission": permission_list if self.get_session('user_type') == '超级管理员' else get_page_permission(
                self.get_session('permission'))
        }
        try:
            if account_email:
                args["email"] = account_email
            self.render("cms/cms_version.html", **args)
        except Exception as e:
            print e
            self.write_response({},0,_err=e)




#子账户管理
class CmsSubAccountHandler(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        self.render("cms/cms_subAccount.html",title="子账户管理")



