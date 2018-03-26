# -*- coding: utf-8 -*-
from tornado import web,ioloop
from config import PORT,setting,BIND_IP
from handlers.main_urls import handlers



def make_app():
    return web.Application(handlers,**setting)


if __name__ == "__main__":
    app = make_app()
    print u'the online teaching web service running'
    app.listen(PORT,BIND_IP)
    ioloop.IOLoop.current().start()
