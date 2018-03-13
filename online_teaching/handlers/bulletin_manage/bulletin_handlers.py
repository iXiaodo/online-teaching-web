# -*- coding: utf-8 -*-
import json
from tornado.gen import coroutine
from datetime import datetime

from handlers.common_handlers.base_handler import BaseHandler
from config import BULLETIN_INFOS,MongoBasicInfoDb
from libs.motor.base import BaseMotor
from models.account import Account
from utils.tools import to_string,to_unicode


#页面
class BulletinInfoPageHandler(BaseHandler):
    @coroutine
    def get(self):
        email = "txq@xx.com"
        try:
            coll = BaseMotor().client[MongoBasicInfoDb][BULLETIN_INFOS]
            res = yield coll.find_one({'_id': email})
            res = res['own_bulletins']
            if not res:
                self.write_response({}, 1, '不存在该账户的表单信息')
                return
            display_lists = []
            for doc in res:
                display_lists.append([doc, res[doc]['pub_time']])

            args = {
                'title': '公告管理',
                'user_type': '教师',
                'username': '教师小汤',
                'bulletins':res,
                'user':email
            }
            self.render("cms/cms_bulletin.html", **args)
        except Exception, e:
            print e


#获取留言数据
class getBulletinInfoHandler(BaseHandler):
    @coroutine
    def get(self):
        main_account = "txq@xx.com"
        try:
            coll = BaseMotor().client[MongoBasicInfoDb][BULLETIN_INFOS]
            res = yield coll.find_one({'_id': main_account})
            res = res['own_bulletins']
            if not res:
                self.write_response({},1,'不存在该账户的表单信息')
                return
            docs = res
            display_lists = []
            for doc in docs:
                display_lists.append([doc,docs[doc]['pub_time']])

            self.write_response(docs)
        except Exception,e:
            self.write_response("", 0, "获取数据失败，请稍后重试")

    @coroutine
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
            self.write_response({}, 0, e)
            return
        if action == 'add':
            bulletin_title = post_data.get('bulletin_title', None)
            bulletin_content = post_data.get('bulletin_content', None)
            bulletin_author = post_data.get('bulletin_author', None)
            bulletin_title = to_unicode(bulletin_title)
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
                                'own_bulletins.{0}'.format(bulletin_title): {
                                    'content': bulletin_content,
                                    'pub_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                    'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                    'is_top': False,
                                    'is_remove': False,
                                    'is_active': True
                                }
                            }
                        })
                    except Exception as e:
                        print e
                        return
                    res_time = res['own_bulletins'][bulletin_title]['pub_time']
                    self.write_response({'pub_time':res_time},1)
                else:
                    self.write_response({},0,'公告标题已经存在，无法重复添加')
                    return
            except Exception as e:
                print e
                return

        elif action == 'del':
            bulletin_title = post_data.get('bulletin_title', None)
            bulletin_title = to_string(bulletin_title)
            bulletin_author = post_data.get('bulletin_author',None)
            if not bulletin_title:
                self.write_response({}, 0, '公告标题为空，无法删除')
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
                print e
                self.write_response({}, 0, '删除公告失败！')
        else:
            pass