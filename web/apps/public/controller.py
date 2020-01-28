# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: controller.py
@Software: PyCharm
@Time :    2019/12/5 上午11:50
"""

import os
from abc import ABC
from tornado.web import StaticFileHandler, stream_request_body
from web.apps.base.controller import BaseRequestHandler
from web.utils.multipart_streamer import MultiPartStreamer
from web.apps.base.status import StatusCode


class UploadItemHandler(StaticFileHandler, ABC):
    async def get(self, path, include_body=True):
        filepath = self.get_absolute_path(self.root, path)
        if os.path.isfile(filepath):
            os.utime(filepath, None)
        await super().get(path, include_body)


@stream_request_body
class FileServerHandler(BaseRequestHandler, ABC):
    def prepare(self):
        if self.request.method.lower() == "post":
            self.request.connection.set_max_body_size(8 << 30)
        try:
            total = int(self.request.headers.get("Content-Length", "0"))
        except KeyError:
            total = 0
        self.ps = MultiPartStreamer(total)

    def data_received(self, chunk):
        self.ps.data_received(chunk)

    async def post(self):
        try:
            self.ps.data_complete()
            parts = self.ps.get_parts_by_name('file')
            filbert = parts[0]
            filbert.f_out.seek(0)
            target_dir = os.path.join('uploads', 'tmp')
            os.makedirs(target_dir, exist_ok=True)
            _, ext = os.path.splitext(filbert.get_filename())
            target_path = os.path.join(target_dir, filbert.md5sum[2:] + ext)
            if not os.path.isfile(target_path):
                filbert.move(target_path)
            url = ''.join([
                target_path.replace("\\", "/")
            ])
            data = dict(url=url, md5sum=filbert.md5sum)
            return self.write_json({
                "code": StatusCode.success.value,
                'msg': "上传成功",
                'data': data
            })
        except Exception as e:
            self.write_json(
                {"code": StatusCode.error.value, "msg": f"上传失败 {e}"})
        finally:
            self.ps.release_parts()
