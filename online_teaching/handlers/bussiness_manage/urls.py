# -*- coding: utf-8 -*-
from role_manage import RoleIndex, RoleInfoHandler

url = [
    (r'^/cms/role_manage',RoleIndex),
    (r'^/cms/role_handler',RoleInfoHandler),
]