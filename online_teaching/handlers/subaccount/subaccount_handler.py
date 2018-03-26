#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import tornado.gen
import tornado.web
from tornado.web import authenticated
from libs.decorator.decorator import permission
from handlers.common_handlers.base_handler import BaseHandler
from models.account import Account, PermissionInsufficientError, AccountNotExistError
from utils.check import check_subaccount_alias, check_subaccount_name, check_email
from utils.tools import to_string
from libs.motor.base import BaseMotor
from config import MongoBasicInfoDb, PERMISSION_NAME_COLLECTION, permission_list
from utils.page import get_page_permission


class GetAccountPermission(BaseHandler):
    """

    """
    @authenticated
    @permission('accountPermissionManage', 'r')
    @tornado.gen.coroutine
    def get(self):
        try:
            main_account = self.get_session('main_account_email')
            coll = BaseMotor().client[MongoBasicInfoDb][PERMISSION_NAME_COLLECTION]
            res = yield coll.find_one({'_id': main_account})
            if not res:
                self.write_response({}, 0, '不存在主账号信息')
                return
            our_permission = [key for key in res['super_admin']]
            account = Account(main_account)
            roles = account.get_roles_and_groups()
            if our_permission and roles:
                self.write_response({
                    'permission': our_permission,
                    'roles': roles
                })
            else:
                self.write_response({}, 0, '获取数据失败')
        except Exception as e:
            self.write_response({}, 0, '获取分组信息失败')


# 子账户的获取
class SubAccountHandler(BaseHandler):
    @authenticated
    @permission('accountPermissionManage', 'r')
    @tornado.gen.coroutine
    def get(self):
        try:
            main_account_id = self.get_session("main_account_email")
            subaccount_id = self.get_session("sub_account")
            subordinate_accounts_info = {}#下属的账户信息
            main_account = Account(main_account_id)
            current_account = Account(main_account_id, subaccount_id)#当前的账户
            accounts_info = [(current_account.account_id, current_account.document)] if current_account.is_subaccount else []
            for subordinate_account_id in current_account.subordinate_accounts_id:
                accounts_info.append((subordinate_account_id, current_account.get_subaccount_document(subordinate_account_id)))
            print current_account.subordinate_accounts_id
            for account_tuple in accounts_info:
                account_id, account_info = account_tuple
                subordinate_accounts_info[account_id] = {
                    "permission": main_account.getSubaccountPermission(account_id),
                    "status": account_info.get("status"),
                    "tel": account_info.get("tel"),
                    "user_email": account_info.get("user_email"),
                    "user_name": account_info.get("user_name"),
                    "role": account_info.get("role"),
                    "group": account_info.get('group')
                }
            self.write_response(subordinate_accounts_info)
        except Exception as e:
            self.write_response("", 0, "获取数据失败，请稍后重试")

    @authenticated
    @permission('accountPermissionManage', 'w')
    @tornado.gen.coroutine
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

    @tornado.gen.coroutine
    def get_group_list(self):
        group_list = []
        user = self.get_session("main_account_email")
        coll = BaseMotor().client[MongoBasicInfoDb][PERMISSION_NAME_COLLECTION]
        idc_group = yield coll.find_one({"_id": user})
        if idc_group:
            for key in idc_group['super_admin']:
                group_list.append(key)
            raise tornado.gen.Return(group_list)
        else:
            raise Exception



class SubAccountPageHandler(BaseHandler):
    @authenticated
    @tornado.gen.coroutine
    @permission('accountPermissionManage', 'r')
    def get(self):
        email = self.get_session("main_account_email")
        account = self.get_session("sub_account")
        args = {
            "title": "子账户管理",
            "user_type": self.get_session("user_type"),
            "email": email,
            "permission": permission_list if self.get_session('user_type') == '超级管理员' else get_page_permission(self.get_session('permission'))
        }
        try:
            if account:
                email = self.get_session("subaccount_email")
                args['email']=email
            self.render("cms/subAccount.html", **args)
        except Exception as e:
            print e
            self.write_response({},0,_err=e)


