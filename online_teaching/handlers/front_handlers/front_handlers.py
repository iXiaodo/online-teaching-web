# -*- coding: utf-8 -*-
from handlers.common_handlers.base_handler import BaseHandler
#首页

class IndexHandler(BaseHandler):
    def get(self):
        self.write("这是前台首页！")