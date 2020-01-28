# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: urls.py
@Software: PyCharm
@Time :    2020/1/28 下午1:58
"""
from web.apps.nosari.controller import NoSariHandler, NoSariNewsHandler, NoSariOverallHandler

urlpatterns = [
    (r'/news', NoSariNewsHandler),
    (r'/overall', NoSariOverallHandler),
    (r'', NoSariHandler)
]
