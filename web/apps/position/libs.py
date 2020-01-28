# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: libs.py
@Software: PyCharm
@Time :    2020/1/28 下午7:33
"""
from web.apps.base.status import StatusCode


async def put_record(self, **kwargs):
    return {"status": True, "code": StatusCode.success.value, "msg": "获取成功"}


async def parser_file_content(self, file_path):
    pass
