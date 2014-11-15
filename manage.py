# coding: utf-8
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from application import create_app
from application.models import db, Blog, Post
from application.utils.blog import grab_by_feed


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
def grab_feed():
    """获取最新feed数据"""
    with app.app_context():
        for blog in Blog.query:
            grab_by_feed(blog)


@manager.command
def remote_grab():
    from celery_proj.tasks import grab

    grab.delay()


@manager.command
def grab_spider():
    """通过spider爬取博文"""
    from spiders import grab_by_spider
    from spiders.livid import LividSpider

    return grab_by_spider(LividSpider)


@manager.command
def test_spider():
    """测试Spider

    将下方的WangYinSpider替换为你写的SPider，
    然后运行python manage.py test_spider即可。

    共有3条测试指令：
        1. test_get_posts: 测试get_posts
        2. test_get_post: 测试get_post
        3. test_format: 测试全部数据的格式

    建议按顺序依次测试：
        运行1（注释2、3），看输出是否正常
        运行2（注释1、3），看输入是否正常
        运行3（注释1、2），看是否通过格式测试
    """
    from spiders.livid import LividSpider

    # LividSpider.test_get_posts()  # 测试get_posts
    #LividSpider.test_get_post()  # 测试get_post
    #LividSpider.test_format()  # 测试全部数据的格式


if __name__ == "__main__":
    manager.run()