# -*- coding: utf-8 -*-
import logging
from tornado.gen import coroutine
from geetest.geetest import GeetestLib
from config import GT_ID,GT_KEY
from base_handler import BaseHandler


# 验证码处理3.0
class PcGetCaptchaHandler(BaseHandler):
    @coroutine
    def get(self):
        user_id = 'test'
        try:
            gt = GeetestLib(GT_ID, GT_KEY)
            status = gt.pre_process(user_id)
            self.session[gt.GT_STATUS_SESSION_KEY] = str(status)
            self.session["user_id"] = user_id
            response_str = gt.get_response_str()
            self.write(response_str)
        except Exception as e:
            logging.exception(e)
            print e
            self.write('对不起，请求验证码异常')

