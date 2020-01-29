# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: urls.py
@Software: PyCharm
@Time :    2020/1/29 上午8:44
"""

from web.apps.gateway.controller import WxGatewayHandler, JsApiHandler
from web.apps.gateway.wx_controller import WxMenuHandler

urlpatterns = [
    (r'/gateway', WxGatewayHandler),
    (r'/JsApi/(.*?)', JsApiHandler),
    (r'/menus', WxMenuHandler)
]