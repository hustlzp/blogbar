# coding: utf-8


def parse_int(integer, default=None):
    """提取整数，若失败则返回default值"""
    try:
        return int(integer)
    except Exception, e:
        return default
