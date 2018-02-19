# -*- coding: utf-8 -*-

from handlers.common_handlers.base_handler import BaseHandler
#首页

class CmsIndexHandler(BaseHandler):
    def get(self):
        self.write("后台首页！")