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
from web.apps.gateway.urls import urlpatterns as wxGateway
from web.apps.user.urls import urlpatterns as user
urlpatterns = list()

urlpatterns += merge_route(common, '')
urlpatterns += merge_route(position, '/area')
urlpatterns += merge_route(no_sari, '/sari')
urlpatterns += merge_route(wxGateway, '/wx')
urlpatterns += merge_route(user, '/user')

