# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: controller.py
@Software: PyCharm
@Time :    2020/1/28 下午1:59
"""

from abc import ABC
from web.apps.base.controller import BaseRequestHandler
from web.apps.base.status import StatusCode


class PositionHandler(BaseRequestHandler, ABC):

    def get(self):
        response = dict(code=StatusCode.success.value, msg="position handler")
        return self.write_json(response)
