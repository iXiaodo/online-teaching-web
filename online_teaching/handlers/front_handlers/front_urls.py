# -*- coding: utf-8 -*-
from front_handlers import IndexHandler,SignInHandler,FrontRegistHandler,ForgetPwdHandler, SignupHandler,testHandler,\
courseCenterHandler

frontUrls = [
    (r"^/$",IndexHandler),
    (r"^/signin",SignInHandler),
    (r"^/regist",FrontRegistHandler),
    (r"^/forgetpwd",ForgetPwdHandler),
    (r"^/logout",SignupHandler),
    (r"^/test",testHandler),
    (r"^/courseCenter",courseCenterHandler),
]