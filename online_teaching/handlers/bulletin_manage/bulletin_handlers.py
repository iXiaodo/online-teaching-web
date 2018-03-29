# -*- coding: utf-8 -*-
import json
from tornado.gen import coroutine
from tornado.web import authenticated
from datetime import datetime
from log import *
from handlers.common_handlers.base_handler import BaseHandler
from config import BULLETIN_INFOS,MongoBasicInfoDb
from libs.motor.base import BaseMotor
from utils.tools import to_string

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



#获取留言数据
class getBulletinInfoHandler(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        email = self.get_session("current_email")
        try:
            bull_coll = BaseMotor().client[MongoBasicInfoDb][BULLETIN_INFOS]
            bull_doc = yield bull_coll.find_one({'_id':email })
            res = bull_doc['own_bulletins']
            if not bull_doc:
                bulletin_data = {
                    "_id":email,
                    "own_bulletins":{}
                }
                res = bull_coll.insert_one(bulletin_data)
                if not res.inserted_id:
                    self.write_response({}, 0, _err='创建数据出错！')
                res = yield bull_coll.find_one({'_id': email})
                res = res['own_bulletins']
            self.write_response(res)
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
            if not bulletin_title:
                self.write_response({}, 0, '公告标题不能为空！')
                return
            if not bulletin_content:
                self.write_response({}, 0, '公告内容不能为空！')
                return
            if not bulletin_author:
                self.write_response({}, 0,'作者获取异常')
                return
            res = yield bulletin_coll.find_one({'_id': bulletin_author})
            try:
                temp_list = []
                for key in res['own_bulletins']:
                    temp_list.append(key)
                if not res['own_bulletins'].has_key(bulletin_title):
                    try:
                        bulletin_coll.update_one({'_id': bulletin_author},{
                            '$set':{
                                'own_bulletins.{0}'.format(to_string(bulletin_title)): {
                                    'content': bulletin_content,
                                    'pub_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                    'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                    'is_top':False,
                                    'is_active':True
                                }
                            }
                        })
                    except Exception as e:
                        logging.exception(e)
                        return
                    self.write_response({},1)
                else:
                    self.write_response({},0,'公告标题已经存在，无法重复添加')
                    return
            except Exception as e:
                logging.exception(e)
                self.write_response({}, 0, e)
                return
        elif action == 'rename':
            old_title_name = post_data.get('old_name', None)
            old_title_name = to_string(old_title_name)
            bulletin_author = post_data.get('bulletin_author',None)
            new_title_name = post_data.get('new_name',None)
            new_title_name = to_string(new_title_name)
            if not (new_title_name and old_title_name):
                self.write_response({}, 0, '标题参数错误，无法删除！')
                return
            try:
                res = bulletin_coll.update_one({'_id':bulletin_author},{
                    '$rename': {
                        'own_bulletins.{0}'.format(old_title_name):'own_bulletins.{0}'.format(new_title_name)
                    }
                })
                if not res:
                    self.write_response({},0,'修改公告标题失败！')
                self.write_response({})
            except Exception as e:
                logging.exception(e)
                self.write_response({}, 0, '修改公告标题失败！')
        elif action == 'del':
            bulletin_title = post_data.get('bulletin_title', None)
            bulletin_title = to_string(bulletin_title)
            bulletin_author = post_data.get('bulletin_author',None)
            if not bulletin_title:
                self.write_response({}, 0, '公告标题为空，无法删除！')
                return
            try:
                res = bulletin_coll.update_one({'_id':bulletin_author},{
                    '$unset': {
                        'own_bulletins.{0}'.format(bulletin_title): ''
                    }
                })
                if not res:
                    self.write_response({},0,'删除公告失败！')
                self.write_response({})
            except Exception as e:
                logging.exception(e)
                self.write_response({}, 0, '删除公告失败！')
        elif action == 'top':
            bulletin_title = post_data.get('bulletin_title', None)
            bulletin_title = to_string(bulletin_title)
            bulletin_author = post_data.get('bulletin_author', None)
            if not bulletin_title:
                self.write_response({}, 0, '公告标题为空，无法操作！')
                return
            try:
                res = bulletin_coll.update({'_id':bulletin_author},{
                    '$set':{
                        'own_bulletins.{0}.{1}'.format(bulletin_title,'update_time'): datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'own_bulletins.{0}.{1}'.format(bulletin_title,'is_top'): True,
                        'own_bulletins.{0}.{1}'.format(bulletin_title,'is_active'): True,
                        'own_bulletins.{0}.{1}'.format(bulletin_title,'top_time'): datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                })
                if not res:
                    self.write_response({},0,'置顶公告失败！')
                self.write_response({})
            except Exception as e:
                logging.exception(e)
                self.write_response({}, 0, '置顶公告失败！！')
        elif action == 'cancel_top':
            bulletin_title = post_data.get('bulletin_title', None)
            bulletin_title = to_string(bulletin_title)
            bulletin_author = post_data.get('bulletin_author', None)
            if not bulletin_title:
                self.write_response({}, 0, '公告标题为空，无法操作！')
                return
            try:
                res = bulletin_coll.update({'_id': bulletin_author}, {
                    '$set': {
                        'own_bulletins.{0}.{1}'.format(bulletin_title, 'update_time'): datetime.now().strftime(
                            '%Y-%m-%d %H:%M:%S'),
                        'own_bulletins.{0}.{1}'.format(bulletin_title, 'is_top'): False,
                        'own_bulletins.{0}.{1}'.format(bulletin_title, 'top_time'):''
                    }
                })
                if not res:
                    self.write_response({}, 0, '取消操作失败！')
                self.write_response({})
            except Exception as e:
                logging.exception(e)
                self.write_response({}, 0, '取消操作失败！')
        elif action == 'modify':
            bulletin_title = post_data.get('bulletin_title', None)
            bulletin_title = to_string(bulletin_title)
            bulletin_author = post_data.get('bulletin_author', None)
            content = post_data.get('content',None)
            is_active = post_data.get('is_active',None)
            is_active = bool(is_active)
            try:
                res = bulletin_coll.update({'_id': bulletin_author}, {
                    '$set': {
                        'own_bulletins.{0}.{1}'.format(bulletin_title, 'update_time'): datetime.now().strftime(
                            '%Y-%m-%d %H:%M:%S'),
                        'own_bulletins.{0}.{1}'.format(bulletin_title, 'is_active'): is_active,
                        'own_bulletins.{0}.{1}'.format(bulletin_title, 'content'):content
                    }
                })
                if not res:
                    print 'not res'
                    self.write_response({}, 0, '修改内容失败！')
                self.write_response({})
            except Exception as e:
                logging.exception(e)
                self.write_response({}, 0, '修改内容失败！')
        else:
            pass