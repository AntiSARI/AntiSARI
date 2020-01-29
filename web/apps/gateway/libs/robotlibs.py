# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: robotlibs.py
@Software: PyCharm
@Time :    2020/1/29 上午8:54
"""
import time
from web.apps.gateway.libs.constant import apply_txt_template, apply_image_template, apply_voice_template


async def robot_ctrl(self, xml):
    msg_type = xml.get('MsgType')
    if msg_type == 'text':
        return await text_apply(xml)
    if msg_type == 'image':
        return await image_apply(xml)
    if msg_type == 'voice':
        return await voice_apply(xml)
    elif msg_type == 'event':
        event = xml.get('Event')
        if event == 'subscribe':
            return await text_apply(xml, "感谢关注本平台")
        elif event == 'unsubscribe':
            return await text_apply(xml, "期待您的再次关注")
        elif event == 'LOCATION':
            return 'success'


async def text_apply(xml, content=None):
    apply = {
        "ToUserName": xml.get('FromUserName'),
        "FromUserName": xml.get('ToUserName'),
        "CreateTime": int(time.time()),
        "Content": xml.get('Content') if not content else content,
    }
    return apply_txt_template.format(**apply)


async def image_apply(xml):
    apply = {
        "ToUserName": xml.get('FromUserName'),
        "FromUserName": xml.get('ToUserName'),
        "CreateTime": int(time.time()),
        "MediaId": xml.get('MediaId'),
    }
    return apply_image_template.format(**apply)


async def voice_apply(xml):
    apply = {
        "ToUserName": xml.get('FromUserName'),
        "FromUserName": xml.get('ToUserName'),
        "CreateTime": int(time.time()),
        "MediaId": xml.get('MediaId'),
    }
    return apply_voice_template.format(**apply)
