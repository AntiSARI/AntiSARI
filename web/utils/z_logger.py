# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: z_logger.py
@Software: PyCharm
@Time :    2019/12/11 下午4:45
"""
import logzero
import logging
import os


def init_logger(filename=None, level='DEBUG', max_bytes=5000, backup_count=3):
    level = getattr(logging, level.upper())
    logzero.loglevel(level)
    if filename:
        filepath = os.path.join(os.getcwd(), filename)
        p = os.path.dirname(filepath)
        if not os.path.exists(p):
            os.mkdir(p)
        else:
            logzero.logfile(filepath, maxBytes=max_bytes, backupCount=backup_count, loglevel=level)
