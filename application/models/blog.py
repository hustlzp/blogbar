# coding: utf-8
import re
import datetime
from lxml import html
from flask import g
from ._base import db

FEED_STATUS_GOOD = 0
FEED_STATUS_BAD = 1
FEED_STATUS_TIMEOUT = 2


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    subtitle = db.Column(db.String(100))
    author = db.Column(db.String(50))

    feed = db.Column(db.String(500))
    feed_timezone_offset = db.Column(db.Integer, default=0)
    feed_version = db.Column(db.String(20))
    feed_status = db.Column(db.Integer, default=FEED_STATUS_GOOD)

    url = db.Column(db.String(200))
    since = db.Column(db.Integer)
    avatar = db.Column(db.String(200))
    keywords = db.Column(db.Text)

    for_special_purpose = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)  # 是否通过审批
    is_protected = db.Column(db.Boolean, default=False)  # 版权保护
    has_spider = db.Column(db.Boolean, default=False)  # 是否通过Spider获取数据
    offline = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime)

    def subscribed_by_user(self):
        if not g.user:
            return False
        return g.user.user_blogs.filter(UserBlog.blog_id == self.id).count() > 0

    def __repr__(self):
        return '<Blog %s>' % self.title


class UserBlog(db.Model):
    """用户订阅博客"""
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    blog = db.relationship('Blog', backref=db.backref('blog_users', lazy='dynamic',
                                                      order_by='desc(UserBlog.created_at)',
                                                      cascade="all, delete, delete-orphan"))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('user_blogs', lazy='dynamic',
                                                      order_by='desc(UserBlog.created_at)',
                                                      cascade="all, delete, delete-orphan"))


class Kind(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    show_order = db.Column(db.Integer, default=0)

    parent_id = db.Column(db.Integer, db.ForeignKey('kind.id'))
    parent = db.relationship("Kind", remote_side=[id],
                             backref=db.backref('children', lazy='dynamic',
                                                order_by='asc(Kind.show_order)'))


class BlogKind(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    show_order = db.Column(db.Integer, default=0)

    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    blog = db.relationship('Blog', backref=db.backref('blog_kinds', lazy='dynamic',
                                                      order_by='asc(BlogKind.show_order)'))

    kind_id = db.Column(db.Integer, db.ForeignKey('kind.id'))
    kind = db.relationship('Kind', backref=db.backref('blog_kinds', lazy='dynamic',
                                                      cascade="all, delete, delete-orphan"))


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
    published_at_exceed = db.Column(db.Boolean, default=False)  # Feed中的published_at是否超出当前时间
    updated_at = db.Column(db.DateTime)
    updated_at_exceed = db.Column(db.Boolean, default=False)

    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    blog = db.relationship('Blog', backref=db.backref('posts', lazy='dynamic',
                                                      order_by='desc(Post.published_at)',
                                                      cascade="all, delete, delete-orphan"))

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

    def collected_by_user(self):
        return g.user and g.user.collected_posts.filter(
            UserCollectPost.post_id == self.id).count() > 0


class UserCollectPost(db.Model):
    """用户收藏博文"""
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', backref=db.backref('collectors', lazy='dynamic',
                                                      order_by='desc(UserCollectPost.created_at)',
                                                      cascade="all, delete, delete-orphan"))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('collected_posts', lazy='dynamic',
                                                      order_by='desc(UserCollectPost.created_at)',
                                                      cascade="all, delete, delete-orphan"))


class UserReadPost(db.Model):
    """用户阅读博文"""
    id = db.Column(db.Integer, primary_key=True)
    unread = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', backref=db.backref('readers', lazy='dynamic',
                                                      order_by='desc(UserReadPost.created_at)',
                                                      cascade="all, delete, delete-orphan"))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('read_posts', lazy='dynamic',
                                                      order_by='desc(UserReadPost.created_at)',
                                                      cascade="all, delete, delete-orphan"))


class GrabLog(db.Model):
    """记录Feed抓取错误"""
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    blog = db.relationship('Blog', backref=db.backref('logs', lazy='dynamic',
                                                      order_by='desc(GrabLog.created_at)',
                                                      cascade="all, delete, delete-orphan"))


class ApprovementLog(db.Model):
    """博客推荐记录"""
    id = db.Column(db.Integer, primary_key=True)
    # 审核状态：1 通过，0 不通过，-1 未审核
    status = db.Column(db.Integer, default=-1)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now)
    ip = db.Column(db.String(100))
    message = db.Column(db.Text)

    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    blog = db.relationship('Blog', backref=db.backref('approvement_logs', lazy='dynamic',
                                                      order_by='desc(ApprovementLog.created_at)',
                                                      cascade="all, delete, delete-orphan"))


def _get_pure_content(content):
    """获取用于摘要的文本"""
    from ..utils.helper import remove_html

    pure_content = remove_html(content)
    pure_content = pure_content.strip().strip('　')  # 去除首位的空格、缩进
    pure_content = pure_content.replace('　', ' ')  # 将缩进替换为空格
    pure_content = re.sub('\s+', ' ', pure_content)  # 将多个空格替换为单个空格
    return pure_content
