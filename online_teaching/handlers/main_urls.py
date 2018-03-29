# -*- coding: utf-8 -*-
from handlers.front_handlers.front_urls import frontUrls
from handlers.cms_handlers.cms_urls import cmsUrls
from handlers.common_handlers.base_handler import BaseHandler
from handlers.bussiness_manage.urls import url as bussiness_urls
from handlers.subaccount.urls import url as subaccount_urls
from handlers.bulletin_manage.urls import url as bulletin_url
from handlers.common_handlers.captcha_handlers import PcGetCaptchaHandler
from handlers.common_handlers.qiniu_handler import get_token

handlers = [
    (r"^/geetest/register", PcGetCaptchaHandler),
    (r"^/cms/get_token/$", get_token),
]
handlers += frontUrls
handlers += cmsUrls
handlers += bussiness_urls
handlers += subaccount_urls
handlers += bulletin_url
handlers += [
    (r".*", BaseHandler),
]