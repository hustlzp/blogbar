# coding: utf-8
from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email, URL


class BlogForm(Form):
    """Form for send email"""
    url = StringField('博客地址', [
        DataRequired('不能为空'),
        URL('格式错误')
    ])
    title = StringField('标题', [DataRequired('不能为空')])
    subtitle = StringField('副标题', description='选填')
    author = StringField('作者', [DataRequired('不能为空')])
    feed = StringField('RSS', description='选填')
