# coding: utf-8
import re
import datetime
from lxml import html
from ._base import db


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    subtitle = db.Column(db.String(100))
    author = db.Column(db.String(50))
    feed = db.Column(db.String(500))
    feed_version = db.Column(db.String(20))
    url = db.Column(db.String(200))
    since = db.Column(db.Integer)
    avatar = db.Column(db.String(200))
    keywords = db.Column(db.Text)

    for_special_purpose = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)  # 是否通过审批
    is_protected = db.Column(db.Boolean, default=False)  # 版权保护
    has_spider = db.Column(db.Boolean, default=False)  # 是否通过Spider获取数据

    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return '<Blog %s>' % self.title


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500))
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    pure_content = db.Column(db.Text)
    keywords = db.Column(db.Text)
    clicks = db.Column(db.Integer, default=0)

    hide = db.Column(db.Boolean, default=False)
    recommend = db.Column(db.Boolean, default=False)
    need_analysis = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    published_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    blog = db.relationship('Blog', backref=db.backref('posts', lazy='dynamic',
                                                      order_by='desc(Post.published_at)'))

    def __setattr__(self, name, value):
        # 每当设置content时，更新pure_content和need_analysis
        if name == 'content':
            pure_content = _get_pure_content(value)
            super(Post, self).__setattr__('pure_content', pure_content)
            super(Post, self).__setattr__('need_analysis', True)
        super(Post, self).__setattr__(name, value)

    def update(self):
        self.pure_content = _get_pure_content(self.content)
        self.need_analysis = True


def _get_pure_content(content):
    doc = html.fromstring(content)  # parse html string
    pure_content = doc.text_content().strip().strip('　')  # 去除首位的空格、缩进
    pure_content = pure_content.replace('　', ' ')  # 将缩进替换为空格
    pure_content = re.sub('\s+', ' ', pure_content)  # 将多个空格替换为单个空格
    return pure_content


class GrabLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    blog = db.relationship('Blog', backref=db.backref('logs', lazy='dynamic',
                                                      order_by='desc(GrabLog.created_at)'))


class ApprovementLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # 审核状态：1 通过，0 不通过，-1 未审核
    status = db.Column(db.Integer, default=-1)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now)
    message = db.Column(db.Text)

    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    blog = db.relationship('Blog', backref=db.backref('approvement_logs', lazy='dynamic',
                                                      order_by='desc(ApprovementLog.created_at)'))