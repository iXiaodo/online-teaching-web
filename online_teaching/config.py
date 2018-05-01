# -*- coding: utf-8 -*-

import os

import uuid,base64

#cookie_secret
COOKIE_SECRET = base64.b64encode(uuid.uuid4().bytes)


PORT = 8000
DEBUG = False
BIND_IP = "127.0.0.1"

MONGO_USE_RS = True
MONGO_RS_HOST_PORT = [
    # ("192.168.1.182", 27017)
    ("192.168.147.132", 27017)
]

#七牛配置
AK = ""
SK = ""

MongodbHost = '192.168.1.182'
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
CMS_USER = "cms_user"
FILES = "files"
ARTICLES = "articles"
permission_list = ['roleGroupManage', 'accountPermissionManage', 'bulletinManage']

LOG_DIR = "./log"  # 日志目录
LOG_FILE = 'online_teaching.log'  # 日志文件

PASSWORD_SALT=''
QQ_EMAIL_PWD = ''
QQ_EMAIL_SQM = ''
setting = {
    "cookie_secret": COOKIE_SECRET,
    "login_url": "/cms/login",
    "xsrf_cookies": False,
    'gzip': True,
    'debug': DEBUG,
    'template_path': os.path.join(os.path.dirname(__file__), "templates"),
    'static_path': os.path.join(os.path.dirname(__file__), "static"),
}

#NUM_PAGE
EVERY_PAGE_NUM = 5

try:
    from local_config import *
except ImportError:
    pass


