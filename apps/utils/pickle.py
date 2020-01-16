# -*- coding:utf-8 -*-
__author__ = 'qing.cai@horizon.ai'

import base64
import pickle


def pickle_dumps_to_str(obj):
    try:
        return base64.encodebytes(pickle.dumps(obj)).decode()
    except pickle.PicklingError:
        pass


def pickle_loads_from_str(obj_str):
    try:
        return pickle.loads(base64.decodebytes(obj_str.encode()))
    except pickle.UnpicklingError:
        pass