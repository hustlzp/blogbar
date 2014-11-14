# coding: utf-8
import HTMLParser
import datetime
from lxml import html, etree
import requests
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from application import create_app
from application.models import db, Blog, Post
from application.utils.blog import grab_blog


# Used by app debug & livereload
PORT = 5000

app = create_app()
manager = Manager(app)

# db migrate commands
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def run():
    """Run app."""
    app.run(port=PORT)


@manager.command
def live():
    """Run livereload server"""
    from livereload import Server
    import formic

    server = Server(app)

    # css
    for filepath in formic.FileSet(include="application/static/css/**/*.css"):
        server.watch(filepath)
    # html
    for filepath in formic.FileSet(include="application/templates/css/**/*.html"):
        server.watch(filepath)
    # js
    for filepath in formic.FileSet(include="application/static/js/**/*.js"):
        server.watch(filepath)
    # image
    for filepath in formic.FileSet(include="application/static/image/**/*.*"):
        server.watch(filepath)

    server.serve(port=PORT)


@manager.command
def createdb():
    """Create database."""
    db.create_all()


@manager.command
def grab():
    """获取最新feed数据"""
    with app.app_context():
        for blog in Blog.query:
            try:
                grab_blog(blog)
            except Exception, e:
                blog.last_status = False
                print blog.title
                print e
            else:
                blog.last_status = True
            db.session.add(blog)
            db.session.commit()


@manager.command
def remote_grab():
    from celery_proj.tasks import grab

    grab.delay()


@manager.command
def grab_wy():
    """爬取王垠的博文"""
    from spiders import grab
    from spiders.wangyin import WangYinSpider

    return grab(WangYinSpider)


@manager.command
def grab_lifesinger():
    """爬取lifesinger的博文"""
    from spiders import grab
    from spiders.lifesinger import LifeSingerSpider

    return grab(LifeSingerSpider)


if __name__ == "__main__":
    manager.run()