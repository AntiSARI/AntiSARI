# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: app_route.py
@Software: PyCharm
@Time :    2020/1/7 下午4:13
"""


def merge_route(urls, sys_prefix):
    """
    :param urls:   路由列表
    :param sys_prefix:   Url前缀
    :return:
    """
    route = list()
    if sys_prefix:
        for url in urls:
            route.append((sys_prefix + url[0], url[1]))
    else:
        route = urls
    return route
