# _*_coding:utf-8_*_
"""
@ProjectName: AntiSARI
@Author:  Javen Yan
@File: form_validate.py
@Software: PyCharm
@Time :    2019/12/9 下午3:51
"""


def validate(keys, payloads):
    """
    :param keys:   验证字段
    :param payloads:   form 提交字段
    :return:
    """
    valid_err = list()
    if isinstance(payloads, list):
        for payload in payloads:
            if not payload:
                valid_err.append({'status': False, 'msg': '参数不能为空'})
            for k, v in payload.items():
                if k not in keys:
                    valid_err.append({'status': False, 'msg': '缺少参数{}, 请补全后重试'.format(k)})
    else:
        if not payloads:
            valid_err.append({'status': False, 'msg': '参数不能为空'})
        for k, v in payloads.items():
            if k not in keys:
                valid_err.append({'status': False, 'msg': '缺少参数{}, 请补全后重试'.format(k)})
    if valid_err:
        return False, valid_err
    else:
        return True, "验证成功"
