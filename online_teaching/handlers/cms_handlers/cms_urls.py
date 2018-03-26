# -*- coding: utf-8 -*-
from cms_handlers import IndexHandler,CmsLoginHandler,CmsModifyPwdHandler,CmsVersionHandler,CmsSubAccountHandler,CmsLogoutHandler


cmsUrls = [
    (r'^/cms/$',IndexHandler),
    (r'^/cms/login',CmsLoginHandler),
    (r'^/cms/logout',CmsLogoutHandler),
    (r'^/cms/modifyPwd/$',CmsModifyPwdHandler),
    (r'^/cms/version/$',CmsVersionHandler),
    (r'^/cms/subAccount/$',CmsSubAccountHandler),
]