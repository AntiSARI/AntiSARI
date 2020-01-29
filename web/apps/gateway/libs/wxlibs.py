# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: wxlibs.py
@Software: PyCharm
@Time :    2020/1/29 上午8:50
"""
import hashlib
import time
from uuid import uuid4
from web.models.form_validate import validate
from web.apps.base.status import StatusCode
from web.settings import wx_token, wx_app_id, wx_app_secret
import httpx as requests
from logzero import logger

from web.utils.cache import get_cache, TICKET


async def check_signature(self, signature, timestamp, nonce):
    tmp_array = [wx_token, timestamp, nonce]
    tmp_array.sort()
    sha1 = hashlib.sha1(''.join(tmp_array).encode())
    hashcode = sha1.hexdigest()
    return hashcode == signature


async def get_access_token(self):
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}".format(wx_app_id,
                                                                                                           wx_app_secret)
    try:
        result = await requests.get(url)
        if result.status_code == 200:
            content = result.json()
            if content.get('errcode') == -1:
                return {"status": False, 'msg': "系统繁忙，此时请开发者稍候再试", "code": StatusCode.error.value}
            if content.get('errcode') == 40001:
                return {"status": False, 'msg': "AppSecret错误或者AppSecret不属于这个公众号，请开发者确认AppSecret的正确性",
                        "code": StatusCode.error.value}
            if content.get('errcode') == 40002:
                return {"status": False, 'msg': "请确保grant_type字段值为client_credential", "code": StatusCode.error.value}
            if content.get('errcode') == 40164:
                return {"status": False, 'msg': "调用接口的IP地址不在白名单中，请在接口IP白名单中进行设置", "code": StatusCode.error.value}
            return {"status": True, 'msg': "获取Token成功", "code": StatusCode.success.value, "data": content}
        else:
            return {"status": False, 'msg': "获取Token失败", "code": StatusCode.error.value}
    except Exception as e:
        logger.exception(e)
        return {"status": False, 'msg': "请求异常", "code": StatusCode.error.value}


async def gen_signature(self, **payload):
    state, msg = validate(['url'], payload)
    if not state:
        return {'status': False, 'msg': '数据入参验证失败', "code": StatusCode.params_error.value}
    else:
        sort_data = dict(noncestr=str(uuid4()),
                         ticket=get_cache(TICKET),
                         timestamp=str(int(time.time())),
                         url=payload.get('url').replace('#', ''))
        sorted(sort_data.keys())
        str1 = ""
        for k, v in sort_data.items():
            str1 += f"{k}={v}&"
        if str1.endswith('&'):
            str1 = str1[:-1]
        sha1 = hashlib.sha1(str1.encode())
        hashcode = sha1.hexdigest()
        content = {
            "timestamp": sort_data.get('timestamp'),
            "nonceStr": sort_data.get('noncestr'),
            "signature": hashcode,
            "appId": wx_app_id
        }
        return {"status": True, 'msg': "业务处理成功", "code": StatusCode.success.value, "data": content}