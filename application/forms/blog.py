# coding: utf-8
import re
from flask import abort
from urlparse import urlparse
from flask_wtf import Form
from wtforms import StringField, TextAreaField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, Email, URL
from ..models import Blog
from ..utils.blog import forbidden_url


def check_url(form, field):
    url = field.data
    url = url.strip()
    if not url:
        return
    result = urlparse(url)
    if result.scheme == "":
        url = "http://%s" % url
    elif result.scheme not in ['http', 'https']:
        raise ValueError('URL格式错误。')
    if '.' not in url:
        raise ValueError('URL格式错误。')
    field.data = url


class AddBlogForm(Form):
    """Form for send email"""
    url = StringField('博客地址', [
        DataRequired('不能为空'),
        check_url,
        URL(message='格式错误')
    ], description='博客 URL 地址')
    title = StringField('标题', [DataRequired('不能为空')], description='标题')
    subtitle = StringField('副标题', description='副标题  /  选填')
    author = StringField('作者', [DataRequired('不能为空')], description='博主')
    feed = StringField('Feed', [check_url], description='RSS 订阅地址  /  选填')
    since = StringField('Since', description='博客从哪一年开始写的，如 2012  /  选填')
    kinds = SelectMultipleField('Kinds', coerce=int)

    def validate_url(self, field):
        url = field.data
        if forbidden_url(url):
            raise ValueError('URL不合法')

        blog = Blog.query.filter(Blog.url == field.data).first()
        if blog:
            raise ValueError('博客URL已存在')


class EditBlogForm(Form):
    """Form for send email"""
    url = StringField('博客地址', [
        DataRequired('不能为空'),
        URL('格式错误'),
        check_url
    ])
    title = StringField('标题', [DataRequired('不能为空')])
    subtitle = StringField('副标题', description='选填')
    author = StringField('作者', [DataRequired('不能为空')])
    feed = StringField('Feed', [check_url], description='选填')
    feed_timezone_offset = StringField('Feed时区')
    since = StringField('Since', description='博客从哪一年开始写的。')
