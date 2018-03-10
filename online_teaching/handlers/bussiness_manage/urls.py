# -*- coding: utf-8 -*-
from role_group_handler import RoleGroupIndex, RoleInfoHandler

url = [
    (r'^/cms/role_group_manage',RoleGroupIndex),
    (r'^/cms/role_handler',RoleInfoHandler),
]