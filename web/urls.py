# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: urls.py
@Software: PyCharm
@Time :    2019/12/5 上午10:41
"""
from web.utils.app_route import merge_route
from web.apps.public.urls import urlpatterns as common
from web.apps.position.urls import urlpatterns as position
from web.apps.nosari.urls import urlpatterns as no_sari
urlpatterns = list()

urlpatterns += merge_route(common, '')
urlpatterns += merge_route(position, '/position')
urlpatterns += merge_route(no_sari, '/sari')

