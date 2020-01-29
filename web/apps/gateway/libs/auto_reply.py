# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: auto_reply.py
@Software: PyCharm
@Time :    2020/1/29 下午5:42
"""
from web.models.databases import MsgType, EventType, ApplyType
from datetime import datetime
from logzero import logger
from web.apps.base.status import StatusCode
from web.models.databases import AuthReplyModel
from web.utils.date2json import to_json
from web.models.form_validate import validate


async def get_constant(self):
    data = {
        "MsgType": MsgType,
        "EventType": EventType,
        "ApplyType": ApplyType
    }
    return {"status": True, "code": StatusCode.success.value, "msg": "获取成功", "data": data}


async def get_auto_replay(self, page, page_size):
    rows = AuthReplyModel.paginate(page, page_size)
    return {"status": True, "code": StatusCode.success.value, "msg": "获取成功", "data": to_json(rows)}


async def add_auto_replay(self, **kwargs):
    keys = ['EventKey', 'EventType', 'ApplyType', 'MsgType', 'EventValue']
    state, msg = validate(keys, kwargs)
    if not state:
        return {'status': False, 'msg': '数据入参验证失败', "code": StatusCode.params_error.value}
    try:
        apply = AuthReplyModel(
            EventKey=kwargs.get('EventKey').strip(),
            EventType=kwargs.get('EventType').strip(),
            ApplyType=kwargs.get('ApplyType').strip(),
            MsgType=kwargs.get('MsgType').strip(),
            EventValue=kwargs.get('EventValue').strip()
        )
        self.db.add(apply)
        self.db.commit()
        return {'status': True, 'msg': '添加成功', "code": StatusCode.success.value}
    except Exception as e:
        logger.error(f"apply insert Error: {str(e)}")
        self.db.rollback()
        return {'status': False, 'msg': '添加失败', "code": StatusCode.db_error.value}


async def delete_auto_replay(self, _id):
    row = AuthReplyModel.by_id(_id)
    if row:
        try:
            self.db.delete(row)
            self.db.commit()
            return {'status': True, 'msg': '删除成功', "code": StatusCode.success.value}
        except Exception as e:
            self.db.rollback()
            logger.error(f"news delete Error: {str(e)}")
            return {'status': False, 'msg': '删除失败', "code": StatusCode.db_error.value}
    return {'status': False, 'msg': '未找到该配置', "code": StatusCode.not_found_error.value}


async def update_auto_replay(self, **kwargs):
    keys = ['id', 'EventKey', 'EventType', 'ApplyType', 'MsgType', 'EventValue', 'createTime', 'updateTime']
    state, msg = validate(keys, kwargs)
    if not state:
        return {'status': False, 'msg': '数据入参验证失败', "code": StatusCode.params_error.value}
    try:
        row = AuthReplyModel.by_id(kwargs.get('id'))
        for k, v in kwargs.items():
            if k not in ['updateTime', 'createTime']:
                setattr(row, k, v)
        row.updateTime = datetime.now()
        self.db.commit()
        return {'status': True, 'msg': '更新成功', "code": StatusCode.success.value}
    except Exception as e:
        logger.error(f"apply update Error: {str(e)}")
        self.db.rollback()
        return {'status': False, 'msg': '更新失败', "code": StatusCode.db_error.value}
