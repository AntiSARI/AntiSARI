# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: cache.py
@Software: PyCharm
@Time :    2020/1/29 上午9:49
"""
import json
import urllib3
from logzero import logger
import time
import os
from web.settings import wx_app_id, wx_app_secret

ACCESS = 'access_token'
TICKET = 'jsapi_ticket'
error_status = [-1, 40001, 40002, 40164, None]


def save_cache(content, cache_type):
    with open(cache_type, 'w+') as f:
        f.write(content)


def get_cache(cache_type=None):
    if not os.path.exists(cache_type):
        exec(cache_type + '()')
        return get_cache(cache_type)
    with open(cache_type) as f:
        content = f.read()
    if content:
        token, expires_at = content.split('|')
        now = int(time.time())
        if int(expires_at) < now:
            exec(cache_type + '()')
            return get_cache(cache_type)
        return token
    else:
        exec(cache_type + '()')
        return get_cache(cache_type)


def jsapi_ticket():
    token = get_cache('access_token')
    logger.info("刷新jsapi_ticket开始")
    url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={}&type=jsapi"\
        .format(token)
    try:
        Pool = urllib3.PoolManager()
        result = Pool.request('GET', url=url)
        if result.status == 200:
            content = json.loads(result.data.decode())
            if content.get('errcode') == 0:
                ticket = content.get('ticket')
                expires_in = int(content.get('expires_in'))
                expires_at = int(time.time())+expires_in
                content = f"{ticket}|{expires_at}"
                save_cache(content, 'jsapi_ticket')
    except Exception as e:
        logger.error("============Refresh JSAPI Ticket Error=========")
        logger.exception(e)
        logger.error("============Refresh JSAPI Ticket Error=========")


def access_token():
    logger.info("刷新Token开始")
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"\
        .format(wx_app_id, wx_app_secret)
    try:
        Pool = urllib3.PoolManager()
        result = Pool.request('GET', url=url)
        if result.status == 200:
            content = json.loads(result.data.decode())
            if content.get('errcode') in error_status:
                token = content.get('access_token')
                expires_in = int(content.get('expires_in'))
                expires_at = int(time.time())+expires_in
                content = f"{token}|{expires_at}"
                save_cache(content, 'access_token')
    except Exception as e:
        logger.error("============Refresh Access Token Error=========")
        logger.exception(e)
        logger.error("============Refresh Access Token Error=========")
