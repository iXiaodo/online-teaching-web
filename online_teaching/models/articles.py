# -*- coding: utf-8 -*-
#作者：xiaodong  

#创建时间：18-4-22   

#日期：上午9:28   

#：IDE：PyCharm

import time
from pymongo import  MongoClient
from config import MongoBasicInfoDb, ARTICLES, MongodbHost,MongodbPort, MongodbAuthDb, MongodbPassword,MongodbUser
from bson import ObjectId
from utils.tools import time_formatting

class Articles_info():
    def __init__(self):
        mongo_client = MongoClient(host=MongodbHost, port=MongodbPort)
        if MongodbUser and MongodbPassword and MongodbAuthDb:
            mongo_client[MongodbAuthDb].authenticate(MongodbUser, MongodbPassword)
        self._mongo_client = mongo_client
        self._articles_collection = self._mongo_client[MongoBasicInfoDb][ARTICLES]

    # 'title':title,
    # 'pub_time':int(time.time()),
    # 'update_time':'',
    # 'is_top':False,
    # 'is_active':True,
    # 'author':author,
    # 'email':email,
    # 'desc':desc,
    # 'thumbnail':thumbnail,
    # 'content':content,
    # 'category':category
    @property
    def get_all_articles(self):
        article_coll = self._articles_collection
        articles = article_coll.find({'is_active':True}).sort([('pub_time',-1)])
        all_articles = []
        for article in articles:
            a_article = []
            a_article.append(str(article['_id']))
            a_article.append(article['title'])
            a_article.append(article['is_top'])
            a_article.append(time_formatting(article['pub_time']))
            a_article.append(article['author'])
            a_article.append(article['email'])
            a_article.append(article['category'])
            content = article['content'][0:120] +'...'
            a_article.append(content)
            a_article.append(article['desc'])
            all_articles.append(a_article)
        return all_articles

    @property
    def by_is_active_sort(self):
        coll = self._articles_collection.find({'is_active': True}).sort([('up_time', -1)]).limit(5)
        if coll:
            article_list = []
            for i in coll:
                i['id'] = str(i['_id'])
                i['pub_time'] = time_formatting(i['pub_time'])
                del i['_id']
                article_list.append(i)
            return article_list
        else:
            return None

if __name__ == "__main__":
    a = Articles_info()
    for i in  a.get_all_articles:
        print i[8]