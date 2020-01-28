# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: base.py
@Software: PyCharm
@Time :    2020/1/7 下午3:45
"""
import importlib
from abc import ABC
import tornado.web
from web.settings import middleware_list as MIDDLEWARE_LIST


class Middleware(object):
    """中间件基类"""

    def process_request(self):
        raise NotImplemented

    def process_response(self):
        raise NotImplemented


class MiddleHandler(tornado.web.RequestHandler, ABC):
    """
      中间件处理基类  顺序执行  中间件
    """

    def initialize(self):
        try:
            self.middleware_list
        except AttributeError:
            self.middleware_list = MIDDLEWARE_LIST

    def prepare(self):
        if self.request.method == "OPTIONS":
            return
        for middleware in self.middleware_list:
            m_path, m_class = middleware.rsplit('.', maxsplit=1)
            mod = importlib.import_module(m_path)
            getattr(mod, m_class).process_request(self)

    def on_finish(self):
        for middleware in self.middleware_list:
            m_path, m_class = middleware.rsplit('.', maxsplit=1)
            mod = importlib.import_module(m_path)
            getattr(mod, m_class).process_response(self)

    def finish(self, chunk=None):
        super(MiddleHandler, self).finish(chunk)
