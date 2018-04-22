# -*- coding: utf-8 -*-
#作者：xiaodong  

#创建时间：18-3-17

#日期：下午5:28
#：IDE：PyCharm
import time
from pymongo import  MongoClient
from config import MongoBasicInfoDb, FILES, MongodbHost,MongodbPort, MongodbAuthDb, MongodbPassword,MongodbUser
from bson import ObjectId
from bulletin import time_formatting

class Files_info():
    def __init__(self,email=None,id=None):
        mongo_client = MongoClient(host=MongodbHost, port=MongodbPort)
        if MongodbUser and MongodbPassword and MongodbAuthDb:
            mongo_client[MongodbAuthDb].authenticate(MongodbUser, MongodbPassword)
        self._mongo_client = mongo_client
        self._files_collection = self._mongo_client[MongoBasicInfoDb][FILES]
        if email:
            self.email = email
        if id:
            self._id = ObjectId(id)



    @property
    def by_email(self):
        coll = self._files_collection.find({'email': self.email})
        if coll:
            file_list = []
            for i in coll:
                i['id'] = str(i['_id'])
                i['up_time'] = time_formatting(i['up_time'])
                del i['_id']
                file_list.append(i)
            return file_list

        else:
            return None

    @property
    def by_is_active(self):
        coll = self._files_collection.find({'is_active': True}).sort([('up_time', -1)])
        if coll:
            file_list = []
            for i in coll:
                file = []
                i['id'] = str(i['_id'])
                i['up_time'] = time_formatting(i['up_time'])
                del i['_id']
                file.append(i['filename'])
                file.append(i['up_time'])
                file.append(i['author'])
                file.append(i['url'])
                file_list.append(file)
            return file_list

        else:
            return None

    @property
    def by_is_active_sort(self):
        coll = self._files_collection.find({'is_active': True}).sort([('up_time', -1)]).limit(5)
        if coll:
            file_list = []
            for i in coll:
                i['id'] = str(i['_id'])
                i['up_time'] = time_formatting(i['up_time'])
                del i['_id']
                file_list.append(i)
            return file_list

        else:
            return None


if __name__ == "__main__":
    email ="xd@xx.com"
    file = Files_info(email=email)
    print file.by_is_active


