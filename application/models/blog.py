# coding: utf-8
import datetime
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
    is_duplicate = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    published_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    blog = db.relationship('Blog', backref=db.backref('posts', lazy='dynamic',
                                                      order_by='desc(Post.published_at)'))


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