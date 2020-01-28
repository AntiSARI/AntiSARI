# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: libs.py
@Software: PyCharm
@Time :    2020/1/28 下午4:38
"""
from web.models.databases import SariRecord
from web.apps.base.status import StatusCode
from web.utils.date2json import to_json


def parse_single_data(rows):
    result = dict(confirmedCount=0,
                  suspectedCount=0,
                  curedCount=0,
                  deadCount=0,
                  cities=[])
    for row in rows:
        result['country'] = row.get('country')
        result['provinceName'] = row.get('provinceName')
        result['provinceShortName'] = row.get('provinceShortName')
        result['confirmedCount'] += int(row.get('confirmedCount'))
        result['suspectedCount'] += int(row.get('suspectedCount'))
        result['curedCount'] += int(row.get('curedCount'))
        result['deadCount'] += int(row.get('deadCount'))
        result['comment'] = row.get('comment', '')
        result['updateTime'] = row.get('updateTime')
        tmp = dict(cityName=row.get('cityName'),
                   confirmedCount=row.get('confirmedCount'),
                   suspectedCount=row.get('suspectedCount'),
                   curedCount=row.get('curedCount'),
                   deadCount=row.get('deadCount')
                   )
        result['cities'].append(tmp)
    return result


async def record_by_province(self, province):
    rows = SariRecord.by_province(province)
    result = parse_single_data(to_json(rows))
    return {"status": True, "code": StatusCode.success.value, "msg": "获取成功", "data": result}


async def records(self):
    rows = SariRecord.all()
    need_parse = dict()
    result = list()
    for row in to_json(rows):
        if not need_parse.get(row.get('provinceName')):
            need_parse.setdefault(row.get('provinceName'), [row])
        else:
            need_parse[row.get('provinceName')].append(row)
    for v in need_parse.values():
        result.append(parse_single_data(v))
    return {"status": True, "code": StatusCode.success.value, "msg": "获取成功", "data": result}
