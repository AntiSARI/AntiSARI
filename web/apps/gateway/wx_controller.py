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
from web.apps.base.status import StatusCode
from web.apps.gateway.libs.auto_reply import get_constant, get_auto_replay, add_auto_replay, delete_auto_replay, \
    update_auto_replay
from web.apps.gateway.libs.menus import add_menu, get_menus, delete_menu
from web.apps.gateway.libs.news_lib import get_news, add_news, delete_new, update_news


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


class WxNewsHandler(BaseRequestHandler, ABC):
    async def get(self):
        response = dict()
        page = int(self.get_argument('page', '1'))
        page_size = int(self.get_argument('page_size', '10'))
        result = await get_news(self, page, page_size)
        response['code'] = result['code']
        response['message'] = result['msg']
        if result['status']:
            response['data'] = result['data']
        return self.write_json(response)

    async def post(self):
        response = dict()
        payload = self.get_payload()
        result = await add_news(self, **payload)
        response['code'] = result['code']
        response['message'] = result['msg']
        return self.write_json(response)

    async def delete(self):
        response = dict()
        _id = self.get_argument('id', None)
        if not _id:
            response['code'] = StatusCode.miss_params_error.value
            response['message'] = "参数缺失"
            return self.write_json(response)
        result = await delete_new(self, _id)
        response['code'] = result['code']
        response['message'] = result['msg']
        return self.write_json(response)

    async def put(self):
        response = dict()
        payload = self.get_payload()
        result = await update_news(self, **payload)
        response['code'] = result['code']
        response['message'] = result['msg']
        return self.write_json(response)


class ConstHandler(BaseRequestHandler, ABC):

    async def get(self):
        response = dict()
        result = await get_constant(self)
        response['code'] = result['code']
        response['message'] = result['msg']
        if result['status']:
            response['data'] = result['data']
        return self.write_json(response)


class AutoReplyHandler(BaseRequestHandler, ABC):
    async def get(self):
        response = dict()
        page = int(self.get_argument('page', '1'))
        page_size = int(self.get_argument('page_size', '10'))
        result = await get_auto_replay(self, page, page_size)
        response['code'] = result['code']
        response['message'] = result['msg']
        if result['status']:
            response['data'] = result['data']
        return self.write_json(response)

    async def post(self):
        response = dict()
        payload = self.get_payload()
        result = await add_auto_replay(self, **payload)
        response['code'] = result['code']
        response['message'] = result['msg']
        return self.write_json(response)

    async def delete(self):
        response = dict()
        _id = self.get_argument('id', None)
        if not _id:
            response['code'] = StatusCode.miss_params_error.value
            response['message'] = "参数缺失"
            return self.write_json(response)
        result = await delete_auto_replay(self, _id)
        response['code'] = result['code']
        response['message'] = result['msg']
        return self.write_json(response)

    async def put(self):
        response = dict()
        payload = self.get_payload()
        result = await update_auto_replay(self, **payload)
        response['code'] = result['code']
        response['message'] = result['msg']
        return self.write_json(response)

