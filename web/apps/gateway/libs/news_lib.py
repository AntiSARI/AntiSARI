# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: news_lib.py
@Software: PyCharm
@Time :    2020/1/29 下午5:25
"""
from datetime import datetime
from logzero import logger
from web.apps.base.status import StatusCode
from web.models.databases import NewsModel
from web.utils.date2json import to_json
from web.models.form_validate import validate


async def get_news(self, page, page_size):
    rows = NewsModel.paginate(page, page_size)
    return {"status": True, "code": StatusCode.success.value, "msg": "获取成功", "data": to_json(rows)}


async def add_news(self, **kwargs):
    keys = ['Title', 'Description', 'Content', 'Url', 'PicUrl']
    state, msg = validate(keys, kwargs)
    if not state:
        return {'status': False, 'msg': '数据入参验证失败', "code": StatusCode.params_error.value}
    try:
        news = NewsModel(
            Title=kwargs.get('Title').strip(),
            Description=kwargs.get('Description').strip(),
            Content=kwargs.get('Content').strip(),
            Url=kwargs.get('Url').strip(),
            PicUrl=kwargs.get('PicUrl').strip()
        )
        self.db.add(news)
        self.db.commit()
        return {'status': True, 'msg': '添加成功', "code": StatusCode.success.value}
    except Exception as e:
        logger.error(f"news insert Error: {str(e)}")
        self.db.rollback()
        return {'status': False, 'msg': '添加失败', "code": StatusCode.db_error.value}


async def delete_new(self, newId):
    row = NewsModel.by_id(newId)
    if row:
        try:
            self.db.delete(row)
            self.db.commit()
            return {'status': True, 'msg': '删除成功', "code": StatusCode.success.value}
        except Exception as e:
            self.db.rollback()
            logger.error(f"news delete Error: {str(e)}")
            return {'status': False, 'msg': '删除失败', "code": StatusCode.db_error.value}
    return {'status': False, 'msg': '未找到该', "code": StatusCode.not_found_error.value}


async def update_news(self, **kwargs):
    keys = ['id', 'Title', 'Description', 'Content', 'Url', 'PicUrl', 'createTime', 'updateTime']
    state, msg = validate(keys, kwargs)
    if not state:
        return {'status': False, 'msg': '数据入参验证失败', "code": StatusCode.params_error.value}
    try:
        row = NewsModel.by_id(kwargs.get('id'))
        for k, v in kwargs.items():
            if k not in ['updateTime', 'createTime']:
                setattr(row, k, v)
        row.updateTime = datetime.now()
        self.db.commit()
        return {'status': True, 'msg': '更新成功', "code": StatusCode.success.value}
    except Exception as e:
        logger.error(f"news update Error: {str(e)}")
        self.db.rollback()
        return {'status': False, 'msg': '更新失败', "code": StatusCode.db_error.value}
