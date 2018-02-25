# -*- coding: utf-8 -*-
from front_handlers import IndexHandler,SignInHandler,SignUpHandler,ForgetPwdHandler


frontUrls = [
    (r"^/$",IndexHandler),
    (r"^/signin$",SignInHandler),
    (r"^/signup$",SignUpHandler),
    (r"^/forgetpwd$",ForgetPwdHandler),
]