# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: controller.py
@Software: PyCharm
@Time :    2019/12/5 上午11:50
"""
from abc import ABC
from web.apps.base.controller import BaseRequestHandler
from web.apps.base.status import StatusCode
from web.apps.nosari.libs import record_by_province, records, news, overalls


class NoSariHandler(BaseRequestHandler, ABC):

    async def get(self):
        response = dict(code=StatusCode.success.value)
        province = self.get_argument('province', None)
        if province:
            result = await record_by_province(self, province)
        else:
            result = await records(self)
        response['code'] = result['code']
        response['message'] = result['msg']
        if result['status']:
            response['data'] = result['data']
        return self.write_json(response)


class NoSariOverSeaHandler(BaseRequestHandler, ABC):

    async def get(self):
        response = dict(code=StatusCode.success.value)
        result = await records(self, True)
        response['code'] = result['code']
        response['message'] = result['msg']
        if result['status']:
            response['data'] = result['data']
        return self.write_json(response)


class NoSariNewsHandler(BaseRequestHandler, ABC):

    async def get(self):
        response = dict()
        page = int(self.get_argument('page', '1'))
        page_size = int(self.get_argument('page_size', '10'))
        position = self.get_argument('province', None)
        result = await news(self, page, page_size, position)
        response['code'] = result['code']
        response['message'] = result['msg']
        if result['status']:
            response['data'] = result['data']
        return self.write_json(response)


class NoSariOverallHandler(BaseRequestHandler, ABC):

    async def get(self):
        response = dict()
        num = int(self.get_argument('num', '1'))
        result = await overalls(self, num)
        response['code'] = result['code']
        response['message'] = result['msg']
        if result['status']:
            response['data'] = result['data']
        return self.write_json(response)
