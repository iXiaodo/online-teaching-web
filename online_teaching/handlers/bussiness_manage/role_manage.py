# coding: utf-8

import json

from tornado.gen import coroutine
from tornado.web import authenticated

from handlers.common_handlers.base_handler import BaseHandler
from utils.tools import to_string
from log import *
from libs.motor.base import BaseMotor
from config import MongoBasicInfoDb, CMS_USER

class RoleIndex(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        try:
            email = self.get_session("current_email")
            args = {
                "title": "角色管理",
                "role": self.get_session("role"),
                "email": email,
                "permission": self.get_session("permission")
            }
            self.render("cms/cms_role_manage.html", **args)
        except Exception as e:
            logging.exception(e)
            self.write_response({},0,_err=e)

class RoleInfoHandler(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        try:
            email = self.get_session("current_email")
            data = {
                "role": self.get_session("role"),
                "email": email,
                "permission": self.get_session("permission")
            }
            if data["permission"] == "super_admin":
                super_coll = BaseMotor().client[MongoBasicInfoDb][CMS_USER]
                super_doc = yield super_coll.find_one({"_id":email})
                data['roles'] = super_doc['own_roles']
            self.write_response(data)
        except Exception as e:
            logging.exception(e)
            self.write_response({}, 0, '获取数据异常')

    @authenticated
    @coroutine
    def post(self):
        post_data = self.request.body
        try:
            post_data = json.loads(post_data)
        except (TypeError, ValueError):
            self.write_response({}, 0, '参数格式错误')
            return
        get_type = post_data.get('type', None)
        action = post_data.get('action', None)
        if not (get_type and action):
            self.write_response({}, 0, '参数错误')
            return
        try:
            email = self.get_session("current_email")
            # main_account = self.get_session('main_account_email')
            # a = Account(main_account)
        except Exception as e:
            logging.exception(e)
            self.write_response({}, 0, '不存在主账号信息')
            return
        if get_type == 'role':
            if action == 'add':
                role_name = post_data.get('role_name', None)
                role_name = to_string(role_name)
                if not role_name:
                    self.write_response({}, 0, '缺少角色名称参数')
                    return
                try:
                    # res = a.add_role(role_name)
                    print res
                    if res[0]:
                        self.write_response({})
                    else:
                        self.write_response({}, 0, res[1])
                except Exception as e:
                    print e
                    self.write_response({}, 0, '添加角色失败')
            elif action == 'modify':
                old_name = post_data.get('old_name', None)
                new_name = post_data.get('new_name', None)
                old_name = to_string(old_name)
                new_name = to_string(new_name)
                if not (old_name and new_name):
                    self.write_response({}, 0, '名称参数错误')
                    return
                try:
                    # res = a.modify_role_name(old_name, new_name)
                    if res[0]:
                        self.write_response({})
                    else:
                        self.write_response({}, 0, res[1])
                except Exception as e:
                    logging.exception(e)
                    self.write_response({}, 0, '添加角色失败')
            elif action == 'del':
                role_name = post_data.get('role_name', None)
                if not role_name:
                    self.write_response({}, 0, '缺少角色名称参数')
                    return
                try:
                    res = a.del_role(role_name)
                    if res[0]:
                        self.write_response({})
                    else:
                        self.write_response({}, 0, res[1])
                except Exception as e:
                    logging.exception(e)
                    self.write_response({}, 0, '删除角色失败')























