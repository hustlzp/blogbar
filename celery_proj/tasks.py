# coding: utf-8
from __future__ import absolute_import
import operator
import traceback
from celery_proj.app import app
from application import create_app
from application.models import db, Blog, GrabLog, Post
from application.utils.blog import grab_by_feed
from spiders import grab_by_spider, spiders


@app.task
def grab():
    """获取最新feed数据"""
    new_posts_count = 0
    flask_app = create_app()

    with flask_app.app_context():
        # 通过feed抓取blog
        for blog in Blog.query:
            if blog.feed and blog.is_approved:
                try:
                    new_posts_count += grab_by_feed(blog)
                except Exception, e:
                    log = GrabLog(message=e, details=traceback.format_exc(), blog_id=blog.id)
                    db.session.add(log)
                    db.session.commit()

        # 通过spider抓取blog
        for spider in spiders:
            try:
                new_posts_count += grab_by_spider(spider)
            except Exception, e:
                blog = Blog.query.filter(Blog.url == spider.url).first_or_404()
                log = GrabLog(message=e, details=traceback.format_exc(), blog_id=blog.id)
                db.session.add(log)
                db.session.commit()
    return new_posts_count
