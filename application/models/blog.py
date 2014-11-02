# coding: utf-8
import datetime
from ._base import db


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    author = db.Column(db.String(50))
    feed = db.Column(db.String(500))
    url = db.Column(db.String(50))
    avatar = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return '<Blog %s>' % self.name


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500))
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    pub_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    blog = db.relationship('Blog', backref=db.backref('quotes', lazy='dynamic',
                                                      order_by='desc(Post.pub_at)'))