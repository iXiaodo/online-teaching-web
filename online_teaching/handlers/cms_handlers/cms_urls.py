# -*- coding: utf-8 -*-
from cms_handlers import CmsIndexHandler,CmsLoginHandler



cmsUrls = [
    (r'^/cms/$',CmsIndexHandler),
    (r'^/cms/login/$',CmsLoginHandler),
]