#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

from tornado.gen import coroutine
from tornado.web import authenticated

from handlers.common_handlers.base_handler import BaseHandler
from utils.check import  check_email
from utils.tools import to_string
from libs.motor.base import BaseMotor
from config import MongoBasicInfoDb
from models.cms_user import CmsUser

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

# 子账户的获取
class SubAccountHandler(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        try:
            email = self.get_session("current_email")
            data = CmsUser().get_easy_permission
            print data
            self.write_response(data)
        except Exception as e:
            self.write_response("", 0, "获取数据失败，请稍后重试")

    @authenticated
    @coroutine
    def post(self):
        try:
            data = self.get_argument('data', None)
            mainSubAccountEmail = self.get_session("main_account_email")
            subaccount_id = self.get_session("sub_account")
            current_account = Account(mainSubAccountEmail, subaccount_id)
            account_info = {}
            if mainSubAccountEmail is None:
                self.write_response(response='', _status=0, _err='获取主账户异常')
                return
            if data is None:
                self.write_response(response='', _status=0, _err='传入参数异常')
                return
            try:
                # 处理传入数据
                json_data = json.loads(data)
                sub_name = ""
                method = json_data["method"]
                if not check_subaccount_name(json_data["sub_name"]):
                    raise Exception
                else:
                    sub_name = json_data["sub_name"]
                if method == 'ban':
                    try:
                        account_info = {
                            "status": json_data["status"]
                        }
                        res = current_account.modify_subaccount(sub_name, account_info)
                    except PermissionInsufficientError:
                        self.write_response("权限不足")
                    except AccountNotExistError:
                        self.write_response("账号不存在")
                    except Exception as e:
                        raise e
                    else:
                        if res:
                            self.write_response("修改子账户信息成功")
                        else:
                            self.write_response("", 0, "修改子账户信息失败")
                else:
                    account_info = {
                        "status": bool(json_data["status"])
                    }

                    main_account = Account(mainSubAccountEmail)
                    all_subaccounts = main_account.all_subaccounts
                    sub_list = [arr[1] for arr in all_subaccounts] if all_subaccounts else []

                    if not check_subaccount_alias(json_data['user_name']):
                        self.write_response({}, 0, '昵称格式有误,昵称为3-16位且只能包含数字，英文，汉字')
                        return
                    else:
                        account_info['user_name'] = json_data['user_name']
                    tel = to_string(json_data.get("tel"))
                    if isinstance(tel, str) and len(tel) == 11 and tel.isalnum():
                        account_info["tel"] = tel
                    else:
                        raise Exception
                    email = json_data["user_email"]
                    if check_email(email):
                        account_info["user_email"] = email
                    else:
                        raise Exception
                    idc_permission = json_data["permission"]
                    group_list = yield self.get_group_list()
                    if not group_list:
                        raise Exception
                    if not isinstance(idc_permission, list):
                        try:
                            idc_permission = json.loads(idc_permission)
                        except (TypeError, ValueError):
                            raise Exception
                    for key in idc_permission:
                        if key[0] not in group_list:
                            raise Exception
                    account_info['permission'] = idc_permission
                    role = to_string(json_data["role"])
                    if role in main_account.get_all_roles():
                        account_info["role"] = role
                    else:
                        raise Exception
                    group = to_string(json_data.get('group', None))
                    if group:
                        flag = main_account.is_exist_group_in_role(role, group)
                        if flag:
                            account_info['group'] = group
                        else:
                            raise Exception
                    elif role == '管理' and not group:
                        pass
                    else:
                        raise Exception
                    if method == 'modify':
                        res = current_account.modify_subaccount(sub_name, account_info)
                        if res:
                            self.write_response("修改子用户信息成功")
                        else:
                            self.write_response("", 0, "修改子账户信息失败")
                    elif method == 'add':
                        if json_data['user_name'] in sub_list:
                            self.write_response({}, 0, '子账号昵称重复，请修改')
                            return
                        password = json_data.get("password")
                        if not (isinstance(password, (str, unicode)) or len(password) != 32):
                            raise Exception
                        account_info["password"] = password
                        res = current_account.add_subaccount(
                            subaccount_id=sub_name,
                            **account_info)
                        if res:
                            self.write_response("添加子账户成功")
                        else:
                            self.write_response("", 0, "添加子账户失败")
                            return
                    elif method == 'delete':
                        self.write_response(response='', _status=0, _err='子账户不可以删除')
                        return
                    else:
                        self.write_response(response='', _status=0, _err='传入method异常')
                        return
            except Exception as e:

                self.write_response(response='', _status=0, _err='传入参数异常')
                return
        except Exception as e:

            self.write_response(response='', _status=0, _err='系统异常')
            return







