# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: urls.py
@Software: PyCharm
@Time :    2020/1/29 上午8:44
"""

from web.apps.gateway.controller import WxGatewayHandler, JsApiHandler

urlpatterns = [
    (r'/gateway', WxGatewayHandler),
    (r'/gateway/JsApi/(.*?)', JsApiHandler)
]