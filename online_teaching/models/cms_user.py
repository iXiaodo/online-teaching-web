# -*- coding: utf-8 -*-
#作者：xiaodong  

#创建时间：18-2-26

#日期：下午5:56   

#：IDE：PyCharm
from pymongo import MongoClient

from config import MongoBasicInfoDb, MongodbHost, MongodbPort, MongodbUser, MongodbPassword, MongodbAuthDb,CMS_USER



class CmsUser():
    def __init__(self,email=None,raw_password=None,new_status=None):
        mongo_client = MongoClient(host=MongodbHost, port=MongodbPort)
        if MongodbUser and MongodbPassword and MongodbAuthDb:
            mongo_client[MongodbAuthDb].authenticate(MongodbUser, MongodbPassword)
        self._mongo_client = mongo_client
        self._cms_user_collection = self._mongo_client[MongoBasicInfoDb][CMS_USER]
        if email:
            self._document = self._cms_user_collection.find_one({'user_email':email})
            self._role = self._document['role']
            self._permission = self._document['permission']
            self._tel = self._document['tel']
            self._user_email = self._document['user_email']
            self._user_name = self._document['user_name']
            self._status = self._document['status']
            self._password = self._document['password']

        if raw_password:
            self._new_password = raw_password
        self._new_status = bool(new_status)

    @property
    def get_doc(self):
        return self._cms_user_collection.find()

    @property
    def get_all_id(self):
        id_list = []
        for key in self.get_doc:
            id_list.append(key['_id'])
        return id_list

    @property
    def get_role(self):
        #返回当前账户的role
        return self._role

    @property
    def get_permission(self):
        # 返回当前账户的permission
        return self._permission

    @property
    def get_easy_permission(self):
        cms_users = self._cms_user_collection.find({'permission':{'$ne':'super_admin'}})
        cms_user_list = []
        if cms_users:
            for user in cms_users:
                cms_user_list.append(user)
            return cms_user_list
        else:
            return None



    #重置密码
    @property
    def reset_pwd(self):
        res = self._cms_user_collection.update_one({'user_email':self._user_email},{
            '$set':{
                '{0}'.format('password'):self._new_password
            }
        })
        if res:
            return True
        else:
            return False


    @property
    def ban_cms_user(self):
        res = self._cms_user_collection.update_one({'user_email': self._user_email}, {
            '$set': {
                '{0}'.format('status'): self._new_status
            }
        })
        if res:
            return True
        else:
            return False



    @property
    def get_permissions(self):
        cms_users = self._cms_user_collection.find_one({'permission': 'super_admin'})
        role_info = {}
        role_info['permissions'] =  cms_users['own_permissions']
        return role_info

#
# a = CmsUser()
# a.email = "dsx@xx.com"
# pwd = 'zzzzzz'
# print a.get_role
'''

    "_id" : "dsx@xx.com", 
    "status" : true, 
    "tel" : "12345678910", 
    "subaccount" : {

    }, 
    "permission" : "admin", 
    "role" : "管理", 
    "password" : "648d187a24cfbc6e8097834bf4891458", 
    "user_name" : "管理小马", 
    "user_email" : "dsx@xx.com"
'''
# pwd = 'zzzzzz'
# print make_password(pwd)
# afdbb4c478b5d047644f5c7abc9471d9
if __name__ == "__main__":
    a = CmsUser()
    print a.get_permission_role