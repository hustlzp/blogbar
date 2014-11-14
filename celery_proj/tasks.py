# coding: utf-8
from __future__ import absolute_import
from celery_proj.app import app
from application import create_app
from application.models import db, Blog
from application.utils.blog import grab_blog
from manage import grab_wy, grab_lifesinger


@app.task
def grab():
    """获取最新feed数据"""
    new_posts_count = 0
    flask_app = create_app()
    with flask_app.app_context():
        for blog in Blog.query:
            try:
                new_posts_count += grab_blog(blog)
            except Exception, e:
                blog.last_status = False
                print ("Failed - %s" % blog.title)
                print e
            else:
                blog.last_status = True
                print ("Success - %s" % blog.title)
            db.session.add(blog)
            db.session.commit()

    # 爬取日志
    try:
        new_posts_count += grab_wy()
        new_posts_count += grab_lifesinger()
    except Exception, e:
        print e

    return new_posts_count