# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: create_db.py
@Software: PyCharm
@Time :    2019/12/5 上午10:46
"""
from web.models.dbSession import engine, ModelBase


def run():
    print('------------create_all-------------')
    ModelBase.metadata.create_all(engine)
    print('------------create_end-------------')


if __name__ == "__main__":
    run()
