# -*- coding: utf-8 -*-
import time
from pymongo import  MongoClient
from config import MongoBasicInfoDb, BULLETIN_INFOS, MongodbHost,MongodbPort, MongodbAuthDb, MongodbPassword,MongodbUser
from bson import ObjectId

class Bulletin_info():
    def __init__(self,email=None,id=None):
        mongo_client = MongoClient(host=MongodbHost, port=MongodbPort)
        if MongodbUser and MongodbPassword and MongodbAuthDb:
            mongo_client[MongodbAuthDb].authenticate(MongodbUser, MongodbPassword)
        self._mongo_client = mongo_client
        self._bulletins_collection = self._mongo_client[MongoBasicInfoDb][BULLETIN_INFOS]
        if email:
            self.email = email
        if id:
            self._id = ObjectId(id)
    @property
    def get_doc(self):
        return self._bulletins_collection.find()


    @property
    def get_all_id(self):
        id_list = []
        for key in self.get_doc:
            id_list.append([key.keys()[0],key.values()[0]])
        return id_list


    @property
    def get_bulletin_detail(self,title=''):
        bulletin_detail = []
        coll = self._bulletins_collection.find_one({"own_bulletins": title})
        return None

    #通过作者获取公告信息
    @property
    def by_author(self):
        coll = self._bulletins_collection.find({'author':self.email})
        if coll:
            return coll
        else:
            return None
    #通过公告id获取公告信息
    @property
    def by_id(self):
        coll = self._bulletins_collection.find({'_id':self._id})
        if coll:
            time_info = time_formatting(coll[0]['pub_time'])
            bulletin = coll[0]
            bulletin['pub_time'] = time_info
            return bulletin
        else:
            return None

    # 置顶加时间排序
    @property
    def by_top_sort(self):
        top_bulletin = []
        coll = self._bulletins_collection.find({'is_top':True}).sort([('top_time',-1)])
        if coll:
            for i in coll:
                i['top_time'] = time_formatting(i['top_time'])
                top_bulletin.append(i)
        if top_bulletin:
            return top_bulletin
        else:
            return None

    # 置顶加时间排序查询条目限制
    @property
    def by_top_limit2(self):
        top_bulletin = []
        coll = self._bulletins_collection.find({'is_top': True}).sort([('top_time', -1)]).limit(2)
        if coll:
            for i in coll:
                i['top_time'] = time_formatting(i['top_time'])
                top_bulletin.append(i)
        if top_bulletin:
            return top_bulletin
        else:
            return None


    #取消置顶加时间排序
    @property
    def by_untop_sort(self):
        untop_bulletin = []
        coll = self._bulletins_collection.find({'is_top':False}).sort([('pub_time',-1)])
        if coll:
            for i in coll:
                i['pub_time'] = time_formatting(i['pub_time'])
                untop_bulletin.append(i)
        if untop_bulletin:
            return untop_bulletin
        else:
            return None

    #选择2条
    @property
    def by_untop_limit2(self):
        untop_bulletin = []
        coll = self._bulletins_collection.find({'is_top': False}).sort([('pub_time', -1)]).limit(2)
        if coll:
            for i in coll:
                i['pub_time'] = time_formatting(i['pub_time'])
                untop_bulletin.append(i)
        if untop_bulletin:
            return untop_bulletin
        else:
            return None

def time_formatting(timeStamp):
    """
    :param timeStamp: 传入的时间戳
    :return: 处理后的时间格式
    """
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

if __name__ == "__main__":
    a = Bulletin_info()
    for i in a.by_top_sort:
        print i
