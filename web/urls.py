# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: urls.py
@Software: PyCharm
@Time :    2019/12/5 上午10:41
"""
from web.utils.app_route import merge_route
from web.apps.common.urls import urlpatterns as common
urlpatterns = list()

urlpatterns += merge_route(common, '')

