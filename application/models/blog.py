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
    is_approved = db.Column(db.Boolean, default=False)
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
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    approved_at = db.Column(db.DateTime)
    is_approved = db.Column(db.Boolean, default=False)
    message = db.Column(db.Text)

    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    blog = db.relationship('Blog', backref=db.backref('approvement_logs', lazy='dynamic',
                                                      order_by='desc(ApprovementLog.created_at)'))