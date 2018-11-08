#coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# 连接数据库的数据
DATABASE = ''
USERNAME = ''
PASSWORD = ''
HOSTNAME = '.0.0.1'
PORT = ''
DATABASE = DATABASE
USERNAME = USERNAME
PASSWORD = PASSWORD
# DB_URI的格式：dialect（mysql/sqlite）+driver://username:password@host:port/database?charset=utf8
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,
                                                              PASSWORD,
                                                              HOSTNAME,
                                                              PORT,
                                                              DATABASE
                                                              )

# engine
engine = create_engine(DB_URI, echo=False)
# sessionmaker生成一个session类
Session = sessionmaker(bind=engine)
dbSession = Session()
