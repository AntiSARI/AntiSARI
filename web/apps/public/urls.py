# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: urls.py
@Software: PyCharm
@Time :    2020/1/28 下午1:56
"""
import os
from web.apps.public.controller import FileServerHandler, UploadItemHandler

urlpatterns = [
    (r'/uploader', FileServerHandler),
    (r"/uploads/(.*)", UploadItemHandler,
     dict(path=os.path.join(os.getcwd(), 'uploads')))
]
