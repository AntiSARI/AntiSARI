# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: databases.py
@Software: PyCharm
@Time :    2019/12/5 上午10:48
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, TEXT, Table, ForeignKey, Boolean, Enum, DateTime, and_
from sqlalchemy.orm import relationship
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


# 公司、员工多对多
CompanyUser = Table(
    'company_user',
    ModelBase.metadata,
    Column('company_id', Integer, ForeignKey("company.id"), nullable=False, primary_key=True),
    Column('user_id', Integer, ForeignKey("user.id"), nullable=False, primary_key=True)
)


class Company(ModelBase):
    __tablename__ = 'company'

    id = Column(Integer, autoincrement=True, primary_key=True)
    companyName = Column(String(128), comment="公司名称", index=True, unique=True)
    companyAddr = Column(String(128), comment="公司地址")
    logoPic = Column(String(255), nullable=True, comment="logo图片地址")
    user = relationship("User", secondary=CompanyUser)
    createTime = Column(DateTime, nullable=True, comment="创建时间")
    updateTime = Column(DateTime, nullable=True, comment="更新时间")

    @classmethod
    def by_id(cls, kid):
        return dbSession.query(cls).filter_by(id=kid).first()

    @classmethod
    def all(cls):
        return dbSession.query(cls).all()

    @classmethod
    def update_and_insert(cls, **kwargs):
        name = kwargs.get('companyName')
        row = dbSession.query(cls) \
            .filter(Company.companyName == name) \
            .first()
        if row:
            logger.debug(f"{name} 已经存在 更新数据")
            try:
                for k, v in kwargs.items():
                    setattr(row, k, v)
                dbSession.commit()
            except Exception as e:
                logger.error("Update Error " + str(e))
        else:
            logger.debug(f"{name} 不存在 新增数据")
            try:
                new_row = Company(**kwargs)
                dbSession.add(new_row)
                dbSession.commit()
            except Exception as e:
                logger.error("Insert Error " + str(e))

    @classmethod
    def by_name(cls, name):
        return dbSession.query(cls)\
            .filter(Company.companyName.like('%{}%'.format(name))).all()

    def to_dict(self):
        return {
            "companyName": self.companyName,
            "companyAddr": self.companyAddr,
            "logoPic": self.logoPic,
            "createTime": self.createTime,
            "updateTime": self.updateTime
        }


class StatusEnum(Enum):
    normal = 0      # 健康
    isolated = 1    # 隔离
    suspected = 2   # 疑似
    confirmed = 3   # 确诊


class User(ModelBase):
    __tablename__ = 'user'

    id = Column(Integer, autoincrement=True, primary_key=True)
    userName = Column(String(32), comment="姓名")
    userPhone = Column(String(32), comment="手机")
    avatarPic = Column(String(255), nullable=True, comment="头像地址")
    is_admin = Column(Boolean, default=False, comment="是否是管理者")     # 注册企业的是管理者
    openId = Column(String(128), comment="微信登录openid")
    # status = Column(Enum(StatusEnum), default=StatusEnum.normal, comment="健康状况")
    company = relationship("Company", secondary=CompanyUser)
    createTime = Column(DateTime, nullable=True, comment="创建时间")
    updateTime = Column(DateTime, nullable=True, comment="更新时间")

    @classmethod
    def by_id(cls, kid):
        return dbSession.query(cls).filter_by(id=kid).first()

    @classmethod
    def all(cls):
        return dbSession.query(cls).all()

    @classmethod
    def update_and_insert(cls, **kwargs):
        name = kwargs.get('userName')
        phone = kwargs.get('userPhone')
        row = dbSession.query(cls) \
            .filter(and_(User.userName == name, User.userPhone == phone)) \
            .first()
        if row:
            logger.debug(f"{name} 已经存在 更新数据")
            try:
                for k, v in kwargs.items():
                    setattr(row, k, v)
                dbSession.commit()
            except Exception as e:
                logger.error("Update Error " + str(e))
        else:
            logger.debug("不存在 新增数据")
            try:
                new_row = User(**kwargs)
                dbSession.add(new_row)
                dbSession.commit()
            except Exception as e:
                logger.error("Insert Error " + str(e))

    @classmethod
    def by_name(cls, name):
        return dbSession.query(cls)\
            .filter(User.userName.like('%{}%'.format(name))).all()

    def to_dict(self):
        return {
            "userName": self.userName,
            "userPhone": self.userPhone,
            "avatarPic": self.avatarPic,
            "is_admin": self.is_admin,
            "openId": self.openId,
            # "status": self.status,
            "createTime": self.createTime,
            "updateTime": self.updateTime
        }


class CheckInRecordModel(ModelBase):
    __tablename__ = 'check_in_record'
    id = Column(Integer, autoincrement=True, primary_key=True)
    userId = Column(String(64), comment="用户ID")
    enterpriseId = Column(String(64), comment="企业id")
    address = Column(String(255), nullable=True, comment="地址")
    latitude = Column(String(64), comment="纬度")
    longitude = Column(String(64), comment="经度")
    status = Column(Integer, default=0, comment="状态")
    createTime = Column(DateTime, nullable=True, comment="创建时间", default=datetime.now)
    updateTime = Column(DateTime, nullable=True, comment="更新时间")

    @classmethod
    def by_id(cls, kid):
        return dbSession.query(cls).filter_by(id=kid).first()

    @classmethod
    def by_user_id(cls, kid, page=1, page_size=10):
        start = page_size * (page - 1)
        end = page * page_size
        return dbSession.query(cls).filter_by(userId=kid).order_by(-cls.createTime).slice(start, end).all()

    @classmethod
    def all(cls):
        return dbSession.query(cls).order_by(-cls.createTime).all()

    @classmethod
    def paginate(cls, page=1, page_size=10, userId=None):
        start = page_size * (page - 1)
        end = page * page_size
        if userId:
            return dbSession.query(cls).filter(CheckInRecordModel.userId == userId).order_by(-cls.createTime).slice(start, end).all()
        else:
            return dbSession.query(cls).order_by(-cls.createTime).slice(start, end).all()

    @property
    def _createTime(self):
        if self.createTime:
            return self.createTime.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def _updateTime(self):
        if self.updateTime:
            return self.updateTime.strftime('%Y-%m-%d %H:%M:%S')

    def to_dict(self):
        return {
            "userId": self.userId,
            "enterpriseId": self.enterpriseId,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "status": self.status,
            "createTime": self._createTime,
            "updateTime": self.updateTime
        }


def EventType():
    return [
        {"label": "点击", "value": "CLICK"},
        {"label": "获取地址", "value": "LOCATION"},
        {"label": "扫码", "value": "SCAN"},
        {"label": "跳转", "value": "VIEW"},
        {"label": "文本", "value": "TEXT"}
    ]


def MsgType():
    return [
        {"label": "文本", "value": "text"},
        {"label": "事件", "value": "event"}
    ]


def ApplyType():
    return [
        {"label": "文本", "value": "text"},
        {"label": "图片", "value": "image"},
        {"label": "新闻", "value": "news"},
        {"label": "链接跳转", "value": "view"}
    ]


class AuthReplyModel(ModelBase):
    __tablename__ = 'auto_reply'
    id = Column(Integer, autoincrement=True, primary_key=True)
    EventKey = Column(String(128), comment="自动回复关键字")
    EventType = Column(String(64), comment="类型")
    ApplyType = Column(String(64), comment="回复类型")
    MsgType = Column(String(64), comment="消息类型")
    EventValue = Column(TEXT, comment="触发返回值")
    createTime = Column(DateTime, nullable=True, comment="创建时间", default=datetime.now)
    updateTime = Column(DateTime, nullable=True, comment="更新时间")

    @classmethod
    def by_id(cls, kid):
        return dbSession.query(cls).filter_by(id=kid).first()

    @classmethod
    def get_one(cls, key, eType, msgType):
        return dbSession.query(cls) \
            .filter(and_(AuthReplyModel.EventKey == key,
                         AuthReplyModel.EventType == eType,
                         AuthReplyModel.MsgType == msgType)) \
            .first()

    @classmethod
    def all(cls):
        return dbSession.query(cls).order_by(-cls.createTime).all()

    @classmethod
    def paginate(cls, page=1, page_size=10):
        start = page_size * (page - 1)
        end = page * page_size
        return dbSession.query(cls).order_by(-cls.createTime).slice(start, end).all()

    @property
    def _createTime(self):
        if self.createTime:
            return self.createTime.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def _updateTime(self):
        if self.updateTime:
            return self.updateTime.strftime('%Y-%m-%d %H:%M:%S')

    def to_dict(self):
        return {
            "id": self.id,
            "EventKey": self.EventKey,
            "EventType": self.EventType,
            "EventValue": self.EventValue,
            "ApplyType": self.ApplyType,
            "createTime": self._createTime,
            "updateTime": self.updateTime
        }


class NewsModel(ModelBase):
    __tablename__ = 'news'
    id = Column(Integer, autoincrement=True, primary_key=True)
    Title = Column(String(128), comment="自动回复关键字")
    Description = Column(TEXT, comment="描述")
    Content = Column(TEXT, comment="内容")
    Url = Column(String(128), comment="连接地址")
    PicUrl = Column(String(128), comment="图片地址")
    createTime = Column(DateTime, nullable=True, comment="创建时间", default=datetime.now)
    updateTime = Column(DateTime, nullable=True, comment="更新时间")

    @classmethod
    def by_id(cls, kid):
        return dbSession.query(cls).filter_by(id=kid).first()

    @classmethod
    def all(cls):
        return dbSession.query(cls).order_by(-cls.createTime).all()

    @classmethod
    def paginate(cls, page=1, page_size=10):
        start = page_size * (page - 1)
        end = page * page_size
        return dbSession.query(cls).order_by(-cls.createTime).slice(start, end).all()

    @property
    def _createTime(self):
        if self.createTime:
            return self.createTime.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def _updateTime(self):
        if self.updateTime:
            return self.updateTime.strftime('%Y-%m-%d %H:%M:%S')

    def to_dict(self):
        return {
            "id": self.id,
            "Title": self.Title,
            "Description": self.Description,
            "Content": self.Content,
            "Url": self.Url,
            "PicUrl": self.PicUrl,
            "createTime": self._createTime,
            "updateTime": self.updateTime
        }