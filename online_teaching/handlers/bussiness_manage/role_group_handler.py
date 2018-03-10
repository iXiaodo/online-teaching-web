# coding: utf-8
from tornado.gen import coroutine
from tornado.web import authenticated
from handlers.common_handlers.base_handler import BaseHandler
from libs.decorator.decorator import permission
from models.account import Account
import json
from config import permission_list
from utils.page import get_page_permission
from utils.tools import to_string,to_unicode

class RoleGroupIndex(BaseHandler):
    @authenticated
    @permission("businessManage", 'r')
    @coroutine
    def get(self):
        args = {
            "title": "角色分组管理",
            "user_type": self.get_session("user_type"),
            "username": self.get_session("main_account_email") + "::" + self.get_session(
                "sub_account") if self.get_session("sub_account") else self.get_session("main_account_email"),
            "subAccount": True if self.get_session('user_type') == '主账号' else
            self.get_session('permission').get('subAccountManage'),
            "permission": permission_list if self.get_session('user_type') == '主账号' else get_page_permission(self.get_session('permission'))
        }
        self.render("cms/role_group_manage.html", **args)


class RoleInfoHandler(BaseHandler):
    @authenticated
    @permission("businessManage", 'r')
    @coroutine
    def get(self):
        try:
            main_account = self.get_session('main_account_email')
            a = Account(main_account)
            data = a.own_roles
            self.write_response(data)
        except Exception as e:
            # logging.exception(e)
            self.write_response({}, 0, '获取数据异常')

    @authenticated
    @permission("businessManage", 'w')
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
            main_account = self.get_session('main_account_email')
            a = Account(main_account)
        except Exception as e:
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
                    res = a.add_role(role_name)
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
                    res = a.modify_role_name(old_name, new_name)
                    if res[0]:
                        self.write_response({})
                    else:
                        self.write_response({}, 0, res[1])
                except Exception as e:
                    print e
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
                    print e
                    self.write_response({}, 0, '删除角色失败')
        elif get_type == 'group':
            if action == 'add':
                role_name = post_data.get('role_name', None)
                group_name = post_data.get('group_name', None)
                group_name = to_string(group_name)
                role_name = to_string(role_name)
                rank = post_data.get('rank', None)
                if not (role_name and group_name and rank):
                    self.write_response({}, 0, '缺少参数')
                    return
                try:
                    rank = int(rank)
                except (TypeError, ValueError):
                    self.write_response({}, 0, '级别值参数错误')
                    return
                try:
                    res = a.add_group_for_role(role_name, group_name, rank)
                    if res[0]:
                        self.write_response({})
                    else:
                        self.write_response({}, 0, res[1])
                except Exception as e:
                    print e
                    self.write_response({}, 0, '添加分组失败')
            elif action == 'modify':
                new_group = post_data.get('new_group', None)
                new_rank = post_data.get('new_rank', None)
                old_group = post_data.get('old_group', None)
                role_name = post_data.get('role_name', None)
                if not (role_name and new_group and new_rank and old_group):
                    self.write_response({}, 0, '缺少参数')
                    return
                try:
                    rank = int(new_rank)
                except (TypeError, ValueError):
                    self.write_response({}, 0, '级别值参数错误')
                    return
                try:
                    res = a.modify_group_for_role(role_name, old_group, new_group, rank)
                    if res[0]:
                        self.write_response({})
                    else:
                        self.write_response({}, 0, res[1])
                except Exception as e:
                    self.write_response({}, 0, '修改分组失败')
            elif action == 'del':
                role_name = post_data.get('role_name', None)
                group_name = post_data.get('group_name', None)
                if not (role_name and group_name):
                    self.write_response({}, 0, '缺少参数')
                    return
                try:
                    res = a.del_group_for_role(role_name, group_name)
                    if res[0]:
                        self.write_response({})
                    else:
                        self.write_response({}, 0, res[1])
                except Exception as e:
                    self.write_response({}, 0, '删除分组失败')






















