# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: controller.py
@Software: PyCharm
@Time :    2020/1/29 上午8:44
"""
from abc import ABC
from logzero import logger
from web.apps.base.controller import BaseRequestHandler
from web.apps.base.status import StatusCode
from web.apps.gateway.libs.robotlibs import robot_ctrl
from web.apps.gateway.libs.wxlibs import check_signature, gen_signature


class WxGatewayHandler(BaseRequestHandler, ABC):

    async def post(self):
        try:
            xml = self.get_xml_json().get('xml')
            result = await robot_ctrl(self, xml)
            return self.write(result)
        except Exception as e:
            logger.exception(e)
            return self.write_json({"code": 10001, "msg": "参数解析失败"})

    async def get(self):
        signature = self.get_argument('signature', '')
        timestamp = self.get_argument('timestamp', '')
        nonce = self.get_argument('nonce', '')
        echo_str = self.get_argument('echostr', '')
        res = await check_signature(self, signature, timestamp, nonce)
        if res:
            return self.write(echo_str)
        else:
            return self.write_json({"code": 10001, "msg": "验证失败"})


class JsApiHandler(BaseRequestHandler, ABC):

    async def post(self, action=None):
        response = dict()
        if action == 'getSignature':
            payloads = self.get_payload()
            result = await gen_signature(self, **payloads)
            response['code'] = result['code']
            response['message'] = result['msg']
            if result['status']:
                response['data'] = result['data']
        else:
            response['code'] = StatusCode.error.value
            response['message'] = "未知操作"
        return self.write_json(response)
