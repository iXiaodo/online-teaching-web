# -*- coding: utf-8 -*-
from cms_handlers import CmsDataManageHandler,CmsLoginHandler,CmsModifyPwdHandler,CmsVersionHandler,CmsSubAccountHandler,CmsLogoutHandler,CmsProfilePageHandler,CmsDataManageInfoHandler


cmsUrls = [
    (r'^/cms/login',CmsLoginHandler),
    (r'^/cms/logout',CmsLogoutHandler),
    (r'^/cms/modifyPwd/$',CmsModifyPwdHandler),
    (r'^/cms/version/$',CmsVersionHandler),
    (r'^/cms/subAccount/$',CmsSubAccountHandler),
    (r'^/cms/$',CmsProfilePageHandler),
    (r'^/cms/dataPage/$',CmsDataManageHandler),
    (r'^/cms/dataInfo/$',CmsDataManageInfoHandler),
]