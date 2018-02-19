# -*- coding: utf-8 -*-
import uuid,base64
import os
cookie_secret = base64.b64encode(uuid.uuid4().bytes)

PORT = 8888
DEBUG = True
BIND_IP = "0.0.0.0"



setting = {
    "cookie_secret": cookie_secret,
    "xsrf_cookies": False,
    'gzip': True,
    'debug': DEBUG,
    'template_path': os.path.join(os.path.dirname(__file__), "templates"),
    'static_path': os.path.join(os.path.dirname(__file__), "static"),
}