# -*- coding: utf-8 -*-

import os
from local_config import *



PORT = 8888
DEBUG = True
BIND_IP = "0.0.0.0"



setting = {
    "cookie_secret": COOKIE_SECRET,
    "xsrf_cookies": True,
    'gzip': True,
    'debug': DEBUG,
    'template_path': os.path.join(os.path.dirname(__file__), "templates"),
    'static_path': os.path.join(os.path.dirname(__file__), "static"),
    # pycket的配置信息
    'pycket':PYCKET,
}