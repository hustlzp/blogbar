# coding: utf-8
from __future__ import absolute_import
from celery_proj.app import app
from application import create_app
from application.models import db, Blog
from application.utils.blog import grab_by_feed


@app.task
def grab():
    """获取最新feed数据"""
    new_posts_count = 0
    flask_app = create_app()
    with flask_app.app_context():
        for blog in Blog.query:
            if blog.feed:
                try:
                    new_posts_count += grab_by_feed(blog)
                except Exception, e:
                    print e
            else:
                pass

    # 爬取blog
    from spiders import grab_by_spider, subclasses

    for subclasse in subclasses:
        try:
            new_posts_count += grab_by_spider(subclasse)
        except Exception, e:
            print e

    return new_posts_count