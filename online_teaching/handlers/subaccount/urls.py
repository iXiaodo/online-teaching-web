#!/usr/bin/python
# -*- coding: utf-8 -*-

from subaccount_handler import SubAccountHandler, GetAccountPermission, SubAccountPageHandler

url = [
    (r"/cms/subaccount", SubAccountHandler),
    (r"/cms/role_group_permission", GetAccountPermission),
    (r"/cms/subAccount", SubAccountPageHandler),
]