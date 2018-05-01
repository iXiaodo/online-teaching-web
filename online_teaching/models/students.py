# -*- coding: utf-8 -*-
#作者：xiaodong  

#创建时间：18-3-20   

#日期：下午9:56   

#：IDE：PyCharm

from pymongo import MongoClient

from config import MongoBasicInfoDb, MongodbHost, MongodbPort, MongodbUser, MongodbPassword, MongodbAuthDb,STUDENTS



class Students():
    def __init__(self):
        mongo_client = MongoClient(host=MongodbHost, port=MongodbPort)
        if MongodbUser and MongodbPassword and MongodbAuthDb:
            mongo_client[MongodbAuthDb].authenticate(MongodbUser, MongodbPassword)
        self._mongo_client = mongo_client
        self._stu_collection = self._mongo_client[MongoBasicInfoDb][STUDENTS]



    @property
    def get_all_stu(self):
        all_stu = self._stu_collection.find({'permission':'student'})
        all_stu_list = []
        for stu in all_stu:
            stu['id'] = stu['_id']
            del stu['_id']
            all_stu_list.append(stu)
        if all_stu_list:
            return all_stu_list
        else:
            return []



if __name__ == "__main__":
    s = Students()
    print s.get_all_stu
