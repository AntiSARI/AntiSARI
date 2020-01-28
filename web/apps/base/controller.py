# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: controller.py
@Software: PyCharm
@Time :    2019/12/5 上午11:50
"""
import os
from abc import ABC
from tornado.escape import json_decode
from web.models.dbSession import dbSession
from web.utils import jsondate
from web.middleware import MiddleHandler
from web.apps.base.status import UserCenterStatusCode, StatusCode
from web.settings import middleware_list as MIDDLEWARE_LIST
from web.utils.tools import aes_tools


class CorsMiddleware(object):
    """
        跨域 中间件
    """

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", '*')
        self.set_header("Access-Control-Allow-Headers", '*')
        self.set_header('Access-Control-Allow-Methods', '*')

    def options(self):
        self.set_status(204)
        self.finish()


class BaseRequestHandler(CorsMiddleware, MiddleHandler, ABC):
    """ 基础加密框架 处理器 """

    def initialize(self):
        super(BaseRequestHandler, self).initialize()
        self.db = dbSession

    def prepare(self):
        super(BaseRequestHandler, self).prepare()

    def write_json(self, data):
        assert isinstance(data, dict)
        self.set_header("Content-Type", "application/json; charset=utf-8")
        content = jsondate.dumps(data)
        self.write(content)

    def get(self):
        response = dict()
        response['code'] = StatusCode.request_method_error.value
        response['message'] = "not support GET method"
        self.set_status(404)
        self.write_json(response)

    def post(self):
        response = dict()
        response['code'] = StatusCode.request_method_error.value
        response['message'] = "not support POST method"
        self.set_status(404)
        self.write_json(response)

    def put(self):
        response = dict()
        response['code'] = StatusCode.request_method_error.value
        response['message'] = "not support PUT method"
        self.set_status(404)
        self.write_json(response)

    def delete(self):
        response = dict()
        response['code'] = StatusCode.request_method_error.value
        response['message'] = "not support DELETE method"
        self.set_status(404)
        self.write_json(response)

    def patch(self):
        response = dict()
        response['code'] = StatusCode.request_method_error.value
        response['message'] = "not support PATCH method"
        self.set_status(404)
        self.write_json(response)

    def write_aes_data(self, data):
        """
        :keyword AES加密
        :param data:
        :return:
        """
        if isinstance(data, dict):
            content = jsondate.dumps(data).encode()
            res = aes_tools.encrypt(content)
        else:
            content = data.encode()
            res = aes_tools.encrypt(content)
        return self.write(res)

    def get_payload(self):
        return json_decode(self.request.body)

    def on_finish(self):
        super(BaseRequestHandler, self).on_finish()
        self.db.close()


class AuthRequestHandler(BaseRequestHandler, ABC):
    """
        认证 Handler
    """
    middleware_list = MIDDLEWARE_LIST + \
        ['web.middleware.middleware.UserAuthMiddleware']


class DefaultHandler(BaseRequestHandler, ABC):
    def get(self):
        self.write_json({
            "code": StatusCode.route_error.value,
            "message": "Sorry! 404 Not found"
        })

    def post(self):
        response = dict()
        response['code'] = StatusCode.route_error.value
        response['message'] = "Sorry! 404 Not found"
        self.set_status(404)
        self.write_json(response)

    def put(self):
        response = dict()
        response['code'] = StatusCode.route_error.value
        response['message'] = "Sorry! 404 Not found"
        self.set_status(404)
        self.write_json(response)

    def delete(self):
        response = dict()
        response['code'] = StatusCode.route_error.value
        response['message'] = "Sorry! 404 Not found"
        self.set_status(404)
        self.write_json(response)

    def patch(self):
        response = dict()
        response['code'] = StatusCode.route_error.value
        response['message'] = "Sorry! 404 Not found"
        self.set_status(404)
        self.write_json(response)
