# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: controller.py
@Software: PyCharm
@Time :    2020/1/28 下午1:59
"""
import os
from abc import ABC

from logzero import logger

from web.apps.base.controller import BaseRequestHandler
from web.apps.base.status import StatusCode
from web.apps.position.libs import put_record, parser_file_content


class PositionHandler(BaseRequestHandler, ABC):
    def prepare(self):
        if self.request.method.lower() == "post":
            self.request.connection.set_max_body_size(8 << 30)

    def get(self):
        response = dict(code=StatusCode.success.value, msg="position handler")
        return self.write_json(response)

    async def post(self):
        response = dict()
        Type = self.get_argument('action', 'single')  # single / multipart
        if Type == 'single':
            #  单条上报
            payload = self.get_payload()
            result = await put_record(self, **payload)
            response['code'] = result['code']
            response['message'] = result['msg']
        else:
            #  文件上报
            upload_file = self.request.files.get('file', None)
            if not upload_file:
                response['code'] = StatusCode.error.value
                response['message'] = "Invalid File Args"
            else:
                try:
                    file_path = None
                    for meta in upload_file:
                        filename = meta['filename']
                        target_dir = os.path.join('uploads', 'tmp')
                        os.makedirs(target_dir, exist_ok=True)
                        file_path = os.path.join('uploads', 'tmp', filename)
                        with open(file_path, 'wb') as up:
                            up.write(meta['body'])
                    result = await parser_file_content(self, file_path)
                    response['code'] = result['code']
                    response['message'] = result['msg']
                except Exception as e:
                    response['code'] = StatusCode.file_save_error.value
                    response['message'] = "文件保存失败"
                    logger.error(f"Upload File Error : {str(e)}")
        return self.write_json(response)
