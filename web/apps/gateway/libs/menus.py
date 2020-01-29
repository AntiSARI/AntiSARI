# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: menus.py
@Software: PyCharm
@Time :    2020/1/29 下午1:37
"""
import json
import httpx as requests
from logzero import logger
from web.apps.base.status import StatusCode
from web.utils.cache import get_cache, ACCESS


async def add_menu(self, **kwargs):
    token = get_cache(ACCESS)
    url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token={}".format(token)
    body = json.dumps(kwargs,ensure_ascii=False).encode('utf-8')
    try:
        result = await requests.post(url, data=body)
        if 300 > result.status_code >= 200:
            content = result.json()
            if content.get('errcode') == 0:
                return {'status': True, 'msg': '创建菜单成功', 'code': StatusCode.success.value}
            else:
                return {'status': False, 'msg': f'创建菜单成失败 {content.get("errmsg")}', 'code': StatusCode.error.value}
        else:
            return {'status': False, 'msg': '创建菜单成失败', 'code': StatusCode.third_api_error.value}
    except Exception as e:
        logger.error(f"Create Menu Request Error : {e}")
        return {'status': False, 'msg': '创建菜单成失败,请求异常', 'code': StatusCode.third_api_error.value}


async def get_menus(self):
    token = get_cache(ACCESS)
    url = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token={}".format(token)
    try:
        result = await requests.get(url)
        if 300 > result.status_code >= 200:
            content = result.json()
            return {'status': True, 'msg': '获取菜单成功', 'code': StatusCode.success.value, "data": content}
        else:
            return {'status': False, 'msg': '获取菜单失败', 'code': StatusCode.third_api_error.value}
    except Exception as e:
        logger.error(f"Create Menu Request Error : {e}")
        return {'status': False, 'msg': '获取菜单失败,请求异常', 'code': StatusCode.third_api_error.value}


async def delete_menu(self):
    token = get_cache(ACCESS)
    url = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token={}".format(token)
    try:
        result = await requests.get(url)
        if 300 > result.status_code >= 200:
            content = result.json()
            if content.get('errcode') == 0:
                return {'status': True, 'msg': '删除菜单成功', 'code': StatusCode.success.value}
            else:
                return {'status': False, 'msg': f'删除菜单失败 {content.get("errmsg")}', 'code': StatusCode.error.value}
        else:
            return {'status': False, 'msg': '删除菜单失败', 'code': StatusCode.third_api_error.value}
    except Exception as e:
        logger.error(f"Create Menu Request Error : {e}")
        return {'status': False, 'msg': '删除菜单失败, 请求异常', 'code': StatusCode.third_api_error.value}
