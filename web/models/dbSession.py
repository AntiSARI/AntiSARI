# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: dbSession.py
@Software: PyCharm
@Time :    2019/12/5 上午10:42
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from web.settings import *

DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(db_username,
                                                              db_password,
                                                              db_hostname,
                                                              db_port,
                                                              db_database
                                                              )

engine = create_engine(DB_URI, echo=False)
Session = sessionmaker(bind=engine)
dbSession = Session()
ModelBase = declarative_base(engine)
