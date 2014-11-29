# coding: utf-8
import datetime
from datetime import timedelta
import json
from math import ceil


def timesince(value):
    """Friendly time gap"""
    # 系统时间是+800，而post保存的时间是UTC时间
    # 故需先后退8小时
    now = datetime.datetime.now() - timedelta(hours=8)

    # 此处做判断是为了保证delta为正值，以免出现不正常的情况
    if now > value:
        delta = now - value
    else:
        delta = value - now

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


def get_keywords(keywords):
    keywords = json.loads(keywords)[:5]
    return ', '.join([keyword for keyword, weight in keywords])


def readtime(content):
    words = len(content)
    return int(ceil(words / 500.0))


def friendly_url(url):
    return url.rstrip('/').replace('http://', '').replace('https://', '')
