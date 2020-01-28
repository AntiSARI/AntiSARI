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
    def update_and_insert(cls, **kwargs):
        province = kwargs.get('provinceName')
        city = kwargs.get('cityName')
        row = dbSession.query(cls) \
            .filter(and_(SariRecord.provinceName.like('%{}%'.format(province)),
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



