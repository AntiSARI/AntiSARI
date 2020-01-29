# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  liyong
@File: libs.py
@Software: PyCharm
@Time :    2020/1/28 下午11:38
"""
from web.models.databases import User, Company
from web.models.form_validate import validate
from web.apps.base.status import StatusCode
from web.utils.date2json import to_json
from datetime import datetime


async def get_user(self, userid=None):
    if userid:
        rows = User.by_id(userid)
    else:
        rows = User.all()

    result = list()
    for row in to_json(rows):
        result.append(row)
    return {"status": True, "code": StatusCode.success.value, "msg": "获取成功", "data": result}


async def get_company(self, name=None):
    if name:
        rows = Company.by_name(name)
    else:
        rows = Company.all()

    result = list()
    for row in to_json(rows):
        result.append(row)
    return {"status": True, "code": StatusCode.success.value, "msg": "获取成功", "data": result}


async def add_user(self, **kwargs):
    """员工注册"""
    keys = ['userName', 'userPhone', 'company_id']
    state, msg = validate(keys, kwargs)
    if not state:
        return {'status': False, 'msg': '数据入参验证失败', "code": StatusCode.params_error.value}
    try:
        company = Company.by_id(kwargs.get('company_id'))
        user = User(
            userName=kwargs.get('userName').strip(),
            userPhone=kwargs.get('userPhone').strip(),
            createTime=datetime.now()
        )
        company.user += [user]
        self.db.add(user)
        self.db.add(company)
        self.db.commit()
        return {'status': True, 'msg': '注册成功', "code": StatusCode.success.value}
    except Exception as e:
        self.db.rollback()
        return {'status': False, 'msg': '注册失败', "code": StatusCode.db_error.value}


async def add_company(self, **kwargs):
    """企业注册"""
    keys = ['companyName', 'companyAddr', 'userName', 'userPhone']
    state, msg = validate(keys, kwargs)
    if not state:
        return {'status': False, 'msg': '数据入参验证失败', "code": StatusCode.params_error.value}
    try:
        user = User(
            userName=kwargs.get('userName').strip(),
            userPhone=kwargs.get('userPhone').strip(),
            is_admin=True,
            createTime=datetime.now()
        )
        company = Company(
            companyName=kwargs.get('companyName').strip(),
            companyAddr=kwargs.get('companyAddr').strip(),
            createTime=datetime.now()
        )
        company.user = [user]
        self.db.add(user)
        self.db.add(company)
        self.db.commit()
        return {'status': True, 'msg': '注册成功', "code": StatusCode.success.value}
    except Exception as e:
        self.db.rollback()
        return {'status': False, 'msg': '注册失败', "code": StatusCode.db_error.value}
