# coding: utf-8

import json
import datetime

TIME_ISO_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'


def _json_decoder(d):
    for key, val in d.items():
        if val == '':
            continue
        try:
            obj = datetime.datetime.fromisoformat(val)
            d[key] = obj.astimezone()
        except (ValueError, TypeError):
            continue

    return d


def loads(s):
    return json.loads(s, object_hook=_json_decoder)


def _data_handler(obj):
    return obj.strftime(TIME_ISO_FORMAT) if isinstance(
        obj, datetime.datetime) else obj


def dumps(data):
    assert isinstance(data, dict)
    return json.dumps(data, default=_data_handler)
