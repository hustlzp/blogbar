# coding: utf-8
import datetime
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
    import HTMLParser
    from lxml import html, etree
    import requests

    new_posts_count = 0

    url = 'http://www.yinwang.org'
    page = requests.get(url)
    tree = html.fromstring(page.text)

    with app.app_context():
        blog = Blog.query.filter(Blog.url == url).first_or_404()

        for item in tree.cssselect('.list-group-item a'):
            title = item.text_content()
            url = item.get('href')

            post = Post.query.filter(Post.unique_id == url).first()

            # 新文章
            if not post:
                post_page = requests.get(url)
                post_tree = html.fromstring(post_page.text)
                content_element = post_tree.cssselect('body')[0]

                # 去除h2标题
                content_element.remove(content_element.cssselect('h2')[0])

                # 获取内容
                content_list = [content_element.text or ''] \
                               + [etree.tostring(child) for child in content_element]
                content = ''.join(content_list)
                html_parser = HTMLParser.HTMLParser()
                content = html_parser.unescape(content)

                # 获取发表日期
                date_list = filter(None, url.split('/'))
                day = int(date_list[-2])
                month = int(date_list[-3])
                year = int(date_list[-4])
                published_at = datetime.datetime(year=year, month=month, day=day)

                post = Post(url=url, unique_id=url, title=title, content=content,
                            published_at=published_at)
                blog.posts.append(post)
                new_posts_count += 1
            db.session.add(blog)
        db.session.commit()
    return new_posts_count


if __name__ == "__main__":
    manager.run()