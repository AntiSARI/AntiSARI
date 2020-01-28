# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: databases.py
@Software: PyCharm
@Time :    2019/12/5 上午10:48
"""
from sqlalchemy import Column, Integer, String, TEXT, and_
from web.models.dbSession import ModelBase, dbSession
import time
from logzero import logger


class SariRecord(ModelBase):
    __tablename__ = 'sari_records'

    id = Column(Integer, autoincrement=True, primary_key=True)
    country = Column(String(32), comment="国家")
    provinceName = Column(String(32), comment="省份")
    provinceShortName = Column(String(32), comment="省份缩写")
    cityName = Column(String(32), comment="城市")
    confirmedCount = Column(Integer, default=0, comment="确诊")
    suspectedCount = Column(Integer, default=0, comment="疑似")
    curedCount = Column(Integer, default=0, comment="治愈")
    deadCount = Column(Integer, default=0, comment="死亡")
    comment = Column(TEXT, nullable=True, comment="备注信息")
    updateTime = Column(Integer, nullable=True, comment="更新时间")

    @classmethod
    def by_id(cls, kid):
        return dbSession.query(cls).filter_by(id=kid).first()

    @classmethod
    def all(cls):
        return dbSession.query(cls).all()

    @classmethod
    def by_country(cls):
        return dbSession.query(cls).filter(SariRecord.country != '中国').all()

    @classmethod
    def update_and_insert(cls, **kwargs):
        province = kwargs.get('provinceName')
        city = kwargs.get('cityName')
        row = dbSession.query(cls) \
            .filter(and_(SariRecord.provinceName == province,
                    SariRecord.cityName == city)) \
            .first()
        if row:
            logger.debug("已经存在 更新数据")
            try:
                for k, v in kwargs.items():
                    setattr(row, k, v)
                dbSession.commit()
            except Exception as e:
                logger.error("Update Error " + str(e))
        else:
            logger.debug("不存在 新增数据")
            try:
                new_row = SariRecord(**kwargs)
                dbSession.add(new_row)
                dbSession.commit()
            except Exception as e:
                logger.error("Insert Error " + str(e))

    @classmethod
    def by_province(cls, province):
        return dbSession.query(cls)\
            .filter(SariRecord.provinceName.like('%{}%'.format(province))).all()

    @property
    def _update_at(self):
        if self.updateTime:
            tmp = time.localtime(self.updateTime)
            return time.strftime("%Y-%m-%d %H:%M:%S", tmp)

    def to_dict(self):
        return {
            "country": self.country,
            "provinceName": self.provinceName,
            "provinceShortName": self.provinceShortName,
            "cityName": self.cityName,
            "confirmedCount": self.confirmedCount,
            "suspectedCount": self.suspectedCount,
            "curedCount": self.curedCount,
            "deadCount": self.deadCount,
            "updateTime": self._update_at
        }


class SariOverall(ModelBase):
    __tablename__ = 'sari_overall'
    id = Column(Integer, autoincrement=True, primary_key=True)
    infectSource = Column(String(255), comment="传染源")
    passWay = Column(String(255), comment="传播途径")
    dailyPic = Column(String(255), comment="图片")
    summary = Column(TEXT, comment="汇总")
    countRemark = Column(String(255), comment="全国疫情信息概览")
    confirmedCount = Column(Integer, default=0, comment="确诊")
    suspectedCount = Column(Integer, default=0, comment="疑似感染人数")
    curedCount = Column(Integer, default=0, comment="治愈")
    deadCount = Column(Integer, default=0, comment="死亡")
    comment = Column(TEXT, nullable=True, comment="备注信息")
    virus = Column(String(255), nullable=True, comment="病毒")
    remark1 = Column(TEXT, nullable=True, comment="备注信息1")
    remark2 = Column(TEXT, nullable=True, comment="备注信息2")
    remark3 = Column(TEXT, nullable=True, comment="备注信息3")
    remark4 = Column(TEXT, nullable=True, comment="备注信息4")
    remark5 = Column(TEXT, nullable=True, comment="备注信息5")
    generalRemark = Column(TEXT, nullable=True, comment="备注信息")
    abroadRemark = Column(TEXT, nullable=True, comment="备注信息")
    updateTime = Column(Integer, nullable=True, comment="更新时间")
    confirmed = Column(Integer, default=0, comment="确诊")
    suspect = Column(Integer, default=0, comment="疑似感染人数")
    cured = Column(Integer, default=0, comment="治愈")
    death = Column(Integer, default=0, comment="死亡")

    @classmethod
    def by_id(cls, kid):
        return dbSession.query(cls).filter_by(id=kid).first()

    @classmethod
    def by_lasted(cls):
        return dbSession.query(cls).order_by(-cls.updateTime).first()

    @classmethod
    def by_limit(cls, num):
        return dbSession.query(cls).order_by(-cls.updateTime).limit(num)

    @property
    def _update_at(self):
        if self.updateTime:
            tmp = time.localtime(self.updateTime)
            return time.strftime("%Y-%m-%d %H:%M:%S", tmp)

    @classmethod
    def update_and_insert(cls, **kwargs):
        infectSource = kwargs.get('infectSource')
        updateTime = int(str(kwargs.get('updateTime'))[:-3]) if kwargs.get('updateTime') else None
        row = dbSession.query(cls) \
            .filter(and_(SariOverall.infectSource == infectSource,
                    SariRecord.updateTime == updateTime)) \
            .first()
        if row:
            logger.debug("头条 已经存在 更新数据")
            try:
                for k, v in kwargs.items():
                    setattr(row, k, v)
                dbSession.commit()
            except Exception as e:
                logger.error("Update Error " + str(e))
        else:
            logger.debug("头条 不存在 新增数据")
            try:
                new_row = SariOverall(**kwargs)
                dbSession.add(new_row)
                dbSession.commit()
            except Exception as e:
                logger.error("Insert Error " + str(e))

    def to_dict(self):
        return {
            "infectSource": self.infectSource,
            "passWay": self.passWay,
            "dailyPic": self.dailyPic,
            "summary": self.summary,
            "countRemark": self.countRemark,
            "confirmedCount": self.confirmedCount,
            "suspectedCount": self.suspectedCount,
            "curedCount": self.curedCount,
            "deadCount": self.deadCount,
            "virus": self.virus,
            "remark1": self.remark1,
            "remark2": self.remark2,
            "remark3": self.remark3,
            "remark4": self.remark4,
            "remark5": self.remark5,
            "generalRemark": self.generalRemark,
            "abroadRemark": self.abroadRemark,
            "confirmed": self.confirmed,
            "suspect": self.suspect,
            "cured": self.cured,
            "death": self.death,
            "updateTime": self._update_at
        }


class SariNews(ModelBase):
    __tablename__ = 'sari_news'
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(128), comment="标题")
    summary = Column(TEXT, comment="概述")
    infoSource = Column(String(64), comment="来源")
    sourceUrl = Column(String(255), comment="来源地址")
    provinceId = Column(String(24), comment="省份地址")
    provinceName = Column(String(128), comment="省份")
    pubDate = Column(Integer, nullable=True, comment="发布时间")

    @classmethod
    def by_id(cls, kid):
        return dbSession.query(cls).filter_by(id=kid).first()

    @classmethod
    def by_lasted(cls):
        return dbSession.query(cls).order_by(-cls.pubDate).first()

    @classmethod
    def all(cls):
        return dbSession.query(cls).all()

    @classmethod
    def paginate(cls, page=1, page_size=10, location=None):
        start = page_size * (page - 1)
        end = page * page_size
        if location:
            return dbSession.query(cls).filter(SariNews.provinceName.like('%{}%'.format(location))).order_by(-cls.pubDate).slice(start, end).all()
        else:
            return dbSession.query(cls).order_by(-cls.pubDate).slice(start, end).all()

    @property
    def _pub_date(self):
        if self.pubDate:
            tmp = time.localtime(self.pubDate)
            return time.strftime("%Y-%m-%d %H:%M:%S", tmp)

    @classmethod
    def update_and_insert(cls, **kwargs):
        title = kwargs.get('title')
        pubDate = int(str(kwargs.get('pubDate'))[:-3]) if kwargs.get('pubDate') else None
        row = dbSession.query(cls) \
            .filter(and_(SariNews.title == title,
                    SariNews.pubDate == pubDate)) \
            .first()
        if row:
            logger.debug("新闻 已经存在 更新数据")
            try:
                for k, v in kwargs.items():
                    setattr(row, k, v)
                dbSession.commit()
            except Exception as e:
                logger.error("Update Error " + str(e))
        else:
            logger.debug("新闻 不存在 新增数据")
            try:
                new_row = SariNews(**kwargs)
                dbSession.add(new_row)
                dbSession.commit()
            except Exception as e:
                logger.error("Insert Error " + str(e))

    def to_dict(self):
        return {
            "pubDate": self._pub_date,
            "title": self.title,
            "summary": self.summary,
            "infoSource": self.infoSource,
            "sourceUrl": self.sourceUrl,
            "provinceId": self.provinceId,
            "provinceName": self.provinceName
        }
