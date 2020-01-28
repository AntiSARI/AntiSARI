# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: status.py
@Software: PyCharm
@Time :    2020/1/8 下午4:01
"""
from enum import IntEnum


class StatusCode(IntEnum):
    success = 10000   # 成功
    error = 10001     # 未知错误
    db_error = 10002  # 数据库操作失败
    miss_params_error = 10004   # 缺少参数
    params_error = 10005  # 参数不合法
    request_method_error = 10006  # 请求方式不正确
    route_error = 10007  # 请求路径不正确
    exist_error = 10008  # 已存在
    not_found_error = 10009  # 不存在
    file_save_error = 10010  # 文件保存失败


class UserCenterStatusCode(StatusCode, IntEnum):
    account_error = 20001  # 账户未找到
    password_error = 20002  # 密码错误
    not_match_error = 20003  # 密码不一致
    account_exist_error = 20004  # 账户已经存在
    miss_token_error = 20005  # 缺少Token
    token_expired_error = 20006  # token 过期
    access_error = 20007  # 没有权限
