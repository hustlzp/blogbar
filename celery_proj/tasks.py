# coding: utf-8
from __future__ import absolute_import
from celery_proj.app import app
from application import create_app
from application.models import db, Blog, GrabLog
from application.utils.blog import grab_by_feed
from spiders import grab_by_spider, subclasses


@app.task
def grab():
    """获取最新feed数据"""
    new_posts_count = 0
    flask_app = create_app()
    with flask_app.app_context():
        # 通过feed抓取blog
        for blog in Blog.query:
            if blog.feed:
                try:
                    new_posts_count += grab_by_feed(blog)
                except Exception, e:
                    log = GrabLog(error=e, blog_id=blog.id)
                    db.session.add(log)

        # 通过spider抓取blog
        for subclass in subclasses:
            try:
                new_posts_count += grab_by_spider(subclass)
            except Exception, e:
                blog = Blog.query.filter(Blog.url == subclass.url).first_or_404()
                log = GrabLog(error=e, blog_id=blog.id)
                db.session.add(log)

        db.session.commit()
    return new_posts_count