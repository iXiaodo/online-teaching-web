# -*- coding: utf-8 -*-
import json
import time
from tornado.gen import coroutine
from tornado.web import authenticated
from datetime import datetime
from log import *
from handlers.common_handlers.base_handler import BaseHandler
from config import BULLETIN_INFOS,MongoBasicInfoDb
from libs.motor.base import BaseMotor
from utils.tools import to_string
from bson import ObjectId
from models.bulletin import Bulletin_info
#页面
class BulletinInfoPageHandler(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        try:
            email = self.get_session("current_email")
            args = {
                'title': '公告管理',
                'role': self.get_session('role'),
                'email': email,
                'permission':self.get_session('permission')
            }
            self.render("cms/cms_bulletin.html", **args)
        except Exception, e:
            logging.exception(e)



#获取公告数据
class getBulletinInfoHandler(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        email = self.get_session("current_email")
        try:
            bull = Bulletin_info(email)
            bull_doc = bull.by_author
            bull_info = []
            if not bull_doc:
                self.write_response({})
            else:
                for i in bull_doc:
                    i['id'] = str(i.pop('_id'))
                    timeStamp = i['pub_time']
                    timeArray = time.localtime(timeStamp)
                    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    i['pub_time'] = otherStyleTime
                    bull_info.append(i)
                self.write_response(bull_info)
        except Exception as e:
            logging.exception(e)
            self.write_response("", 0, "获取数据失败，请稍后重试")

    @coroutine
    @authenticated
    def post(self):
        post_data = self.request.body
        try:
            post_data = json.loads(post_data)
        except (TypeError, ValueError):
            self.write_response({}, 0, '参数格式错误')
            return
        get_type = post_data.get('type', None)
        action = post_data.get('action', None)
        if not (get_type and action):
            self.write_response({}, 0, '参数错误')
            return
        try:
            bulletin_coll = BaseMotor().client[MongoBasicInfoDb][BULLETIN_INFOS]
        except Exception as e:
            logging.exception(e)
            self.write_response({}, 0, e)
            return
        if action == 'add':
            bulletin_title = post_data.get('bulletin_title', None)
            bulletin_content = post_data.get('bulletin_content', None)
            bulletin_author = post_data.get('bulletin_author', None)
            bulletin_type = post_data.get('bulletin_type', None)
            if not bulletin_title:
                self.write_response({}, 0, '公告标题不能为空！')
                return
            if not bulletin_content:
                self.write_response({}, 0, '公告内容不能为空！')
                return
            if not bulletin_author:
                self.write_response({}, 0,'作者获取异常！')
                return
            if not bulletin_type:
                self.write_response({}, 0,'公告类型获取有误！')
                return
            res = yield bulletin_coll.find_one({'_id': bulletin_author})
            try:
                insert_info = {
                    'title':bulletin_title,
                    'author':bulletin_author,
                    'type':bulletin_type,
                    'content': bulletin_content,
                    'pub_time': int(time.time()),
                    'update_time': '',
                    'is_top': False,
                    'is_active': True
                }
                res = bulletin_coll.insert_one(insert_info)
                if res:
                    self.write_response({})
                else:
                    self.write_response({},0,'公告创建失败')
            except Exception as e:
                logging.exception(e)
                self.write_response({}, 0, e)
                return
        elif action == 'rename':
            old_title_name = post_data.get('old_name', None)
            old_title_name = to_string(old_title_name)
            id = post_data.get('id',None)
            if not id:
                self.write_response({}, 0, '标题id获取异常！')
                return
            new_title_name = post_data.get('new_name',None)
            new_title_name = to_string(new_title_name)
            if not (new_title_name and old_title_name):
                self.write_response({}, 0, '标题参数错误，无法删除！')
                return
            try:
                res = bulletin_coll.update_one({'_id':ObjectId(id)},{
                    '$set': {
                        '{0}'.format('title'):new_title_name,
                        '{0}'.format('pub_time'):int(time.time())
                    }
                })
                if not res:
                    self.write_response({},0,'修改公告标题失败！')
                self.write_response({})
            except Exception as e:
                logging.exception(e)
                self.write_response({}, 0, '修改公告标题失败！')
        elif action == 'del':
            id = post_data.get('id',None)
            if not id:
                self.write_response({}, 0, '公告id为空，无法删除！')
                return
            try:
                res = bulletin_coll.update_one({'_id':ObjectId(id)},{
                    '$unset': {
                        'title':'',
                        'author':'',
                        'type':'',
                        'content': '',
                        'pub_time': '',
                        'update_time': '',
                        'is_top': '',
                        'is_active': ''
                    }
                })
                if not res:
                    self.write_response({},0,'删除公告失败！')
                self.write_response({})
            except Exception as e:
                logging.exception(e)
                self.write_response({}, 0, '删除公告失败！')
        elif action == 'top':
            id = post_data.get('id', None)
            if not id:
                self.write_response({}, 0, '公告id获取异常，无法操作！')
                return
            try:
                res = bulletin_coll.update({'_id':ObjectId(id)},{
                    '$set':{
                        '{0}'.format('update_time'): int(time.time()),
                        '{0}'.format('is_top'): True,
                        '{0}'.format('is_active'): True,
                        '{0}'.format('top_time'): int(time.time())
                    }
                })
                if not res:
                    self.write_response({},0,'置顶公告失败！')
                self.write_response({})
            except Exception as e:
                logging.exception(e)
                self.write_response({}, 0, '置顶公告失败！！')
        elif action == 'cancel_top':
            id = post_data.get('id', None)

            if not id:
                self.write_response({}, 0, '公告id获取异常，无法操作！')
                return
            try:
                res = bulletin_coll.update({'_id': ObjectId(id)}, {
                    '$set':{
                        '{0}'.format('update_time'): int(time.time()),
                        '{0}'.format('is_top'): False,
                        '{0}'.format('is_active'): True,
                        '{0}'.format('top_time'): ''
                    }
                })
                if not res:
                    self.write_response({}, 0, '取消操作失败！')
                self.write_response({})
            except Exception as e:
                logging.exception(e)
                self.write_response({}, 0, '取消操作失败！')
        elif action == 'modify':
            content = post_data.get('content',None)
            is_active = post_data.get('is_active',None)
            is_active = bool(is_active)
            id = post_data.get('id',None)
            if not id:
                self.write_response({}, 0, '公告id获取失败，无法修改！')
                return
            if not content:
                self.write_response({}, 0, '公告内容获取失败，无法修改！')
                return
            try:
                res = bulletin_coll.update_one({'_id': ObjectId(id)}, {
                    '$set': {
                        '{0}'.format('update_time'): int(time.time()),
                        '{0}'.format('is_active'): is_active,
                        '{0}'.format('content'):content
                    }
                })
                if res:
                    self.write_response({})
                else:
                    self.write_response({}, 0, '修改内容失败！')

            except Exception as e:
                logging.exception(e)
                self.write_response({}, 0, '修改内容失败！')
        else:
            pass