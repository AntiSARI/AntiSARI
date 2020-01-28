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
from web.models.databases import SariRecord, SariOverall, SariNews
from web.settings import api_url
from datetime import datetime


class SariDataCollector(object):
    """
       定时拉取全国疫情数据缓存到数据库
    """
    conn = None  # mongo 连接

    def __init__(self, api=api_url, init=False):
        self.log = logger
        self.api = api
        self.init = init

    @property
    def area_url(self):
        if self.init:
            return self.api + '/area?latest=0'
        else:
            return self.api + '/area'

    @property
    def news_url(self):
        if self.init:
            return self.api + '/news?num=1000'
        else:
            return self.api + '/news'

    @property
    def overall_url(self):
        if self.init:
            return self.api + '/overall?latest=0'
        else:
            return self.api + '/overall'

    def _connect_mongo(self):
        pass

    def _fetch_data(self, url):
        result = None
        try:
            req = request.Request(url=url, method='GET')
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
            tmp = dict()
            tmp['country'] = result.get('country')
            tmp['provinceName'] = result.get('provinceName')
            tmp['provinceShortName'] = result.get('provinceShortName')
            tmp['comment'] = result.get('comment')
            tmp['updateTime'] = int(str(result.get('updateTime'))[:-3]) if result.get('updateTime') else None
            if result.get('country') != "中国":
                tmp['cityName'] = result.get('operator')
                tmp['confirmedCount'] = result.get('confirmedCount')
                tmp['suspectedCount'] = result.get('suspectedCount')
                tmp['curedCount'] = result.get('curedCount')
                tmp['deadCount'] = result.get('deadCount')
                new_results.append(tmp)
            else:
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

    def _save_data_overall(self, overalls):
        for overall in overalls:
            overall['updateTime'] = int(str(overall.get('updateTime'))[:-3]) if overall.get('updateTime') else None
            self.log.debug(f"{overall.get('infectSource')} - {overall.get('updateTime')} saving")
            SariOverall.update_and_insert(**overall)

    def _save_data_news(self, news):
        for new in news:
            new['pubDate'] = int(str(new.get('pubDate'))[:-3]) if new.get('pubDate') else None
            self.log.debug(f"{new.get('title')} - {new.get('pubDate')} saving")
            SariNews.update_and_insert(**new)

    def run(self):
        self.log.info(f"Fetch Data Begin At : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        areas = self._fetch_data(self.area_url)
        if areas:
            records = self._clean_data(areas)
            self._save_data(records)

        overall = self._fetch_data(self.overall_url)
        if overall:
            self._save_data_overall(overall)

        news = self._fetch_data(self.news_url)
        if news:
            self._save_data_news(news)

        self.log.info(f"Fetch Data End At : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

