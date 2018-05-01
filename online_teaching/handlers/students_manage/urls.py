# -*- coding: utf-8 -*-
from stu_manage import StudentIndex, StuInfoHandler

url = [
    (r'^/cms/stu_manage',StudentIndex),
    (r'^/cms/stu_handler',StuInfoHandler),
]