# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: collector.py
@Software: PyCharm
@Time :    2020/1/28 下午2:22
"""
import json
from logzero import logger
from urllib import request
from web.models.databases import SariRecord
from web.settings import collector_url
from datetime import datetime


class SariDataCollector(object):
    """
       定时拉取全国疫情数据缓存到数据库
    """
    conn = None  # mongo 连接

    def __init__(self, api=collector_url):
        self.log = logger
        self.api = api

    def _connect_mongo(self):
        pass

    def _fetch_data(self):
        result = None
        try:
            req = request.Request(url=self.api, method='GET')
            response = request.urlopen(req)
            if response.status == 200:
                result = json.loads(response.read().decode('utf-8'))
        except Exception as e:
            self.log.error("Error: " + str(e))
        return result.get('results') if result else None

    @staticmethod
    def _clean_data(results):
        new_results = list()
        for result in results:
            for i in result.get('cities') if result.get('cities') else []:
                tmp = dict()
                tmp['country'] = result.get('country')
                tmp['provinceName'] = result.get('provinceName')
                tmp['provinceShortName'] = result.get('provinceShortName')
                tmp['comment'] = result.get('comment')
                tmp['updateTime'] = int(str(result.get('updateTime'))[:-3]) if result.get('updateTime') else None
                tmp['cityName'] = i.get('cityName')
                tmp['confirmedCount'] = i.get('confirmedCount')
                tmp['suspectedCount'] = i.get('suspectedCount')
                tmp['curedCount'] = i.get('curedCount')
                tmp['deadCount'] = i.get('deadCount')
                new_results.append(tmp)
        return new_results

    def _save_data(self, records):
        for record in records:
            self.log.debug(f"{record.get('provinceName')} - {record.get('cityName')} saving")
            SariRecord.update_and_insert(**record)

    def run(self):
        self.log.info(f"Fetch Data Begin At : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        rows = self._fetch_data()
        if rows:
            records = self._clean_data(rows)
            self._save_data(records)
        self.log.info(f"Fetch Data End At : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

