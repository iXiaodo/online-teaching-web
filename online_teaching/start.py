# -*- coding: utf-8 -*-
from tornado import web,ioloop
from tornado.options import define,options
from config import PORT,setting,BIND_IP
from handlers.main_urls import handlers
from libs.db import create_tables
from local_config import create_super_user


define("ct",  default=False, help="create tables", type=bool)
define("cs",  default=False, help="create super_user", type=bool)


def make_app():
    return web.Application(handlers,**setting)





if __name__ == "__main__":
    options.parse_command_line()
    # 创建表
    if options.ct:
        create_tables.run()

    #创建超级管理员
    if options.cs:
        create_super_user()
        print u"恭喜您，超级管理员创建成功！"
    app = make_app()
    print u'the online teaching web service running'
    app.listen(PORT,BIND_IP)
    ioloop.IOLoop.current().start()
