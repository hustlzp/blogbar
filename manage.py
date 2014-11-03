# coding: utf-8
import feedparser
from time import mktime
from datetime import datetime
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from application import create_app
from application.models import db, Blog, Post


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
def feed():
    """获取最新feed数据"""
    with app.app_context():
        for blog in Blog.query:
            result = feedparser.parse(blog.feed)
            if 'updated_parsed' in result.feed:
                blog.updated_at = _get_time(result.feed.updated_parsed)
            if 'id' in result.feed:
                blog.unique_id = result.feed.id
            elif 'link' in result.feed:
                blog.unique_id = result.feed.link
            blog.feed_version = result.version
            if 'subtitle' in result.feed:
                blog.subtitle = result.feed.subtitle

            db.session.add(blog)
            print(blog.title)

            # 最新博文
            for entry in result.entries:
                identity = entry.id if 'id' in entry else entry.link
                post = Post.query.filter(Post.unique_id == identity).first()
                if not post:
                    post = Post(title=entry.title, url=entry.link, unique_id=identity)
                    if 'updated_parsed' in entry:
                        post.updated_at = _get_time(entry.updated_parsed)

                    if 'content' in entry:
                        if isinstance(entry.content, list):
                            post.content = entry.content[0].value
                        else:
                            post.content = entry.content
                    elif 'summary' in entry:
                        post.content = entry.summary

                    db.session.add(post)
                    print(post.title)
        db.session.commit()


def _get_time(time_struct):
    return datetime.fromtimestamp(mktime(time_struct))


if __name__ == "__main__":
    manager.run()