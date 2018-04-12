# -*- coding: utf-8 -*-
from pymongo import  MongoClient
from config import MongoBasicInfoDb, BULLETIN_INFOS, MongodbHost,MongodbPort, MongodbAuthDb, MongodbPassword,MongodbUser

class Bulletin_info():
    def __init__(self):
        mongo_client = MongoClient(host=MongodbHost, port=MongodbPort)
        if MongodbUser and MongodbPassword and MongodbAuthDb:
            mongo_client[MongodbAuthDb].authenticate(MongodbUser, MongodbPassword)
        self._mongo_client = mongo_client
        self._bulletins_collection = self._mongo_client[MongoBasicInfoDb][BULLETIN_INFOS]


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
    def get_all_bulletin_info(self):
        title_list = []
        for i in self.get_all_id:
            coll = self._bulletins_collection.find_one({i[0]:i[1]})
            doc = coll['own_bulletins']
            for key in doc:
                if key:
                    title_list.append([key,doc[key]['pub_time'],doc[key]['is_top']])
        return title_list


    @property
    def get_top_list(self):
        bulletin_top_list = []
        all_bulletins = self.get_all_bulletin_info
        for bulletin in all_bulletins:
            if bulletin[2] is True:
                bulletin_top_list.append(bulletin)
        return bulletin_top_list

    @property
    def get_untop_list(self):
        bulletin_top_list = []
        all_bulletins = self.get_all_bulletin_info
        for bulletin in all_bulletins:
            if bulletin[2] is False:
                bulletin_top_list.append(bulletin)
        return bulletin_top_list

    @property
    def get_bulletin_detail(self,title=''):
        bulletin_detail = []
        coll = self._bulletins_collection.find_one({"own_bulletins": title})


# a = Bulletin_info()
# title = u'考试通知1'
# print a.get_bulletin_detail(title)