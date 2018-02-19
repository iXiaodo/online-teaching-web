# -*- coding: utf-8 -*-
from handlers.front_handlers.front_urls import frontUrls
from handlers.cms_handlers.cms_urls import cmsUrls
from handlers.common_handlers.base_handler import BaseHandler

handlers = [

]
handlers += frontUrls
handlers += cmsUrls
handlers += [
    (r".*", BaseHandler),
]