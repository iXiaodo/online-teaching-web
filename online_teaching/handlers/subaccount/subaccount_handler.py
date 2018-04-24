#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import time
from tornado.gen import coroutine
from tornado.web import authenticated

from handlers.common_handlers.base_handler import BaseHandler
from utils.hashers import  make_password
from utils.tools import to_string
from models.cms_user import CmsUser,MongoBasicInfoDb
from libs.motor.base import BaseMotor
from log import *
from config import CMS_USER,STUDENTS

class SubAccountPageHandler(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        try:
            email = self.get_session("current_email")
            permission = self.get_session("permission")
            args = {
                "title": "CMS用户管理",
                "role": self.get_session("role"),
                "permission": permission,
                "email":email
            }
            self.render("cms/subAccount.html", **args)
        except Exception as e:
            print e
            self.write_response({},0,_err=e)


#权限/角色获取
class permissionRoleHandler(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        try:
            cms = CmsUser()
            data = cms.get_permissions
            if not data:
                self.write_response({},0,'获取权限信息出错')
            else:
                self.write_response(data)
        except Exception as e:
            logging.exception(e)

# 子账户的获取
class SubAccountHandler(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        try:
            email = self.get_session("current_email")
            cms_user = CmsUser(email=email)
            permission = cms_user.get_permission
            if not email:
                self.write_response({},0,'帐号信息出错！')
                return
            if not permission:
                self.write_response({},0,'权限获取异常！')
                return
            if permission == "super_admin":
                data = cms_user.get_easy_permission
                if not data:
                    self.write_response({},0,'查询出错')
                else:
                    self.write_response(data)
            else:
                self.write_response({})
        except Exception as e:
            self.write_response("", 0, "获取数据失败，请稍后重试")

    @authenticated
    @coroutine
    def post(self):
        try:
            post_data = self.request.body
            try:
                data = json.loads(post_data)
            except (TypeError, ValueError):
                self.write_response({}, 0, '参数格式错误')
                return
            action = data.get('action', None)
            if not action:
                self.write_response({}, 0, '获取操作失败！')
                return
            if action == 'ban':
                email = data.get('email',None)
                if not email:
                    self.write_response({},0,'邮箱账户获取出错!')
                    return
                try:
                    cms = CmsUser(email=email, new_status=False)
                    if cms.ban_cms_user:
                        self.write_response({})
                        return
                    else:
                        self.write_response({}, 0, '禁用失败!')
                        return
                except Exception as e:
                    logging.exception(e)
            elif action == 'start_use':
                email = data.get('email',None)
                if not email:
                    self.write_response({},0,'邮箱账户获取出错!')
                    return
                try:
                    cms = CmsUser(email=email, new_status=True)
                    if cms.ban_cms_user:
                        self.write_response({})
                        return
                    else:
                        self.write_response({}, 0, '启用失败!')
                        return
                except Exception as e:
                    logging.exception(e)
            elif action == 'add':
                email = data.get('email', None)
                password = data.get('password', None)
                tel = data.get('tel', None)
                permission = data.get('permission', None)
                username = data.get('username', None)
                if not (email and password and tel and permission and username):
                    self.write_response({},0,'缺少用户信息!')
                    return
                role = ''
                if permission == 'admin':
                    role = u'管理'
                elif permission == 'student':
                    role = u'学生'
                else:
                    role = u'老师'
                # 学生用户
                insert_doc = {
                    "_id": email,
                    "status": True,
                    "password": make_password(password),
                    "avator": "",
                    "create_time": int(time.time()),
                    "permission": permission,
                    "tel": tel,
                    "role": role,
                    "user_name": username,
                    "user_email": email,
                    "stu_num": ""
                }
                if permission != 'student':
                    try:
                        cms_coll = BaseMotor().client[MongoBasicInfoDb][CMS_USER]
                        cms_doc = yield cms_coll.find_one({'user_email': email})
                        if not cms_doc:
                            res = cms_coll.insert_one(insert_doc)
                            if not res:
                                self.write_response({},0,'用户添加失败!')
                                return
                            else:
                                self.write_response({})
                                return
                        else:
                            self.write_response({}, 0, '邮箱账户已存在!')
                            return
                    except Exception as e:
                        logging.exception(e)

                #其它用户
                else:
                    try:
                        stu_coll = BaseMotor().client[MongoBasicInfoDb][STUDENTS]
                        stu_doc = yield stu_coll.find_one({'email': email})
                        if not stu_doc:
                            res = stu_coll.insert_one(insert_doc)
                            if not res:
                                self.write_response({},0,'用户添加失败!')
                            else:
                                self.write_response({})
                        else:
                            self.write_response({}, 0, '邮箱账户已存在!')
                            return
                    except Exception as e:
                        logging.exception(e)


        except Exception as e:
            logging.exception(e)
            self.write_response(response='', _status=0, _err='系统异常')
            return







