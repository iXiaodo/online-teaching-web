#!/usr/bin/python
# -*- coding: utf-8 -*-

from subaccount_handler import SubAccountHandler, SubAccountPageHandler, permissionRoleHandler

url = [
    (r"/cms/subaccount", SubAccountHandler),
    (r"/cms/subAccount", SubAccountPageHandler),
    (r"/cms/get_rolesPermissions/$", permissionRoleHandler),
]