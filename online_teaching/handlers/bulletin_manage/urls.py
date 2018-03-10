# -*- coding: utf-8 -*-
from bulletin_handlers import BulletinInfoPageHandler, getBulletinInfoHandler


url = [
    (r'^/cms/bulletinPage/$',BulletinInfoPageHandler),
    (r'^/cms/bulletinInfo/$',getBulletinInfoHandler),
]