# coding: utf-8
import datetime
import lxml.html


def timesince(value):
    """Friendly time gap"""
    now = datetime.datetime.now()
    delta = now - value
    if delta.days > 365:
        return '%d 年前' % (delta.days / 365)
    if delta.days > 30:
        return '%d 个月前' % (delta.days / 30)
    if delta.days > 0:
        return '%d 天前' % delta.days
    if delta.seconds > 3600:
        return '%d 小时前' % (delta.seconds / 3600)
    if delta.seconds > 60:
        return '%d 分钟前' % (delta.seconds / 60)
    return '刚刚'
