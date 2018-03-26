# -*- coding: utf-8 -*-

import os



COOKIE_SECRET = ''



PORT = 8000
DEBUG = False
BIND_IP = "127.0.0.1"

MONGO_USE_RS = True
MONGO_RS_HOST_PORT = [
    ("127.0.0.1", 27017)
]

MongodbHost = '127.0.0.1'
MongodbPort = 27017
MongodbAuthDb = "admin"
MongodbUser = ''
MongodbPassword = ''
MongoBasicInfoDb = ""
USER_NAME_COLLECTION = 'user'
PERMISSION_NAME_COLLECTION = 'permission'
OPEN_ID_COLLECTION = "open_id"
BULLETIN_INFOS = "bulletin_infos"
STUDENTS = "students"
FRONT_USER = "front_user"
permission_list = ['roleGroupManage', 'accountPermissionManage', 'bulletinManage']

LOG_DIR = "./log"  # 日志目录
LOG_FILE = 'online_teaching.log'  # 日志文件

PASSWORD_SALT=''

setting = {
    "cookie_secret": COOKIE_SECRET,
    "login_url": "/cms/login",
    "xsrf_cookies": False,
    'gzip': True,
    'debug': DEBUG,
    'template_path': os.path.join(os.path.dirname(__file__), "templates"),
    'static_path': os.path.join(os.path.dirname(__file__), "static"),
}

try:
    from local_config import *
except ImportError:
    pass


