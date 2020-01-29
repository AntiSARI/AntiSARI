# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: robotlibs.py
@Software: PyCharm
@Time :    2020/1/29 上午8:54
"""
import time
from web.apps.gateway.libs.constant import apply_txt_template, apply_image_template,\
    apply_view_template, apply_news_template_start, apply_news_template_item, apply_news_template_end
from web.models.databases import AuthReplyModel, NewsModel


async def robot_ctrl(self, xml):
    msg_type = xml.get('MsgType')
    if msg_type == 'text':
        content = xml.get('Content')
        row = AuthReplyModel.get_one(content, 'TEXT', msg_type)
        if row:
            return await replay_msg(row, xml)
        else:
            return await text_apply(xml, "很抱歉, 没有找到您想要的信息")
    elif msg_type == 'event':
        event = xml.get('Event')
        if event == 'subscribe':
            return await text_apply(xml, "感谢您关注本平台")
        elif event == 'unsubscribe':
            return await text_apply(xml, "期待您的再次关注")
        else:
            row = AuthReplyModel.get_one(xml.get('EventKey'), event, msg_type)
            if row:
                return await replay_msg(row, xml)
            else:
                return await text_apply(xml, "很抱歉, 没有找到您想要的信息")
    else:
        return await text_apply(xml, "很抱歉, 该公众号暂不支持此项内容 ")


async def replay_msg(row, xml):
    apply_type = row.ApplyType
    apply_value = row.EventValue
    if apply_value:
        if apply_type == 'text':
            return await text_apply(xml, apply_value)
        elif apply_type == 'image':
            return await image_apply(xml, apply_value)
        elif apply_type == 'news':
            return await news_apply(xml, apply_value)
        elif apply_type == 'view':
            return await view_apply(xml, apply_value)
    else:
        return await text_apply(xml, '很抱歉, 没有找到您想要的信息')


async def text_apply(xml, content=None):
    apply = {
        "ToUserName": xml.get('FromUserName'),
        "FromUserName": xml.get('ToUserName'),
        "CreateTime": int(time.time()),
        "Content": xml.get('Content') if not content else content,
    }
    return apply_txt_template.format(**apply)


async def image_apply(xml, image_id=None):
    apply = {
        "ToUserName": xml.get('FromUserName'),
        "FromUserName": xml.get('ToUserName'),
        "CreateTime": int(time.time()),
        "MediaId": xml.get('MediaId')
    }
    if image_id:
        apply['MediaId'] = image_id
    return apply_image_template.format(**apply)


async def view_apply(xml, url):
    apply = {
        "ToUserName": xml.get('FromUserName'),
        "FromUserName": xml.get('ToUserName'),
        "CreateTime": int(time.time()),
        "EventKey": url
    }
    return apply_view_template.format(**apply)


async def news_apply(xml, apply_value):
    news = apply_value.split(',')
    apply = {
        "ToUserName": xml.get('FromUserName'),
        "FromUserName": xml.get('ToUserName'),
        "CreateTime": int(time.time()),
        "ArticleCount": len(news)
    }
    start = apply_news_template_start.format(**apply)
    items = ""
    for new in news:
        row = NewsModel.by_id(new)
        if row:
            _new = row.to_dict()
            body_tmp = apply_news_template_item.format(**_new)
            items += body_tmp
    return start + items + apply_news_template_end

