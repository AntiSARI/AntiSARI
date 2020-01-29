# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: wx_controller.py
@Software: PyCharm
@Time :    2020/1/29 下午1:34
"""
from abc import ABC

from web.apps.base.controller import BaseRequestHandler
from web.apps.gateway.libs.menus import add_menu, get_menus, delete_menu


class WxMenuHandler(BaseRequestHandler, ABC):

    async def get(self):
        response = dict()
        result = await get_menus(self)
        response['code'] = result['code']
        response['message'] = result['msg']
        if result['status']:
            response['data'] = result['data']
        return self.write_json(response)

    async def post(self):
        response = dict()
        payload = self.get_payload()
        result = await add_menu(self, **payload)
        response['code'] = result['code']
        response['message'] = result['msg']
        return self.write_json(response)

    async def delete(self):
        response = dict()
        result = await delete_menu(self)
        response['code'] = result['code']
        response['message'] = result['msg']
        return self.write_json(response)
