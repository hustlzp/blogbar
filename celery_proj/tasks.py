# coding: utf-8
from __future__ import absolute_import
from fabric.api import shell_env
from celery_proj.app import app
from application import create_app
from application.models import db, Blog
from application.utils.blog import grab_blog


@app.task
def grab():
    """获取最新feed数据"""
    with shell_env(MODE='PRODUCTION'):
        flask_app = create_app()
        with flask_app.app_context():
            for blog in Blog.query:
                try:
                    grab_blog(blog)
                except Exception, e:
                    blog.last_status = False
                    print ("Failed - %s" % blog.title)
                    print e
                else:
                    blog.last_status = True
                    print ("Success - %s" % blog.title)
                db.session.add(blog)
                db.session.commit()