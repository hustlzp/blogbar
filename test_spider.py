# coding: utf-8
"""
Usage:
    test_spider.py get_posts
    test_spider.py get_post
    test_spider.py all
"""
from docopt import docopt
from spiders.wangyin import WangYinSpider as TargetSpider


def test_spider(args):
    """Spider测试程序

    需要将上方的spiders.wangyin替换为你写的模块名，
    将WangYinSpider替换为你写的Spider类。

    共有3条测试指令：

        $ python test_spider.py get_posts
            测试get_posts

        $ python test_spider.py get_posts
            测试get_post

        $ python test_spider.py all
            测试所有返回数据的格式

    建议按顺序依次测试。
    """
    if args['get_posts']:
        TargetSpider.test_get_posts()
    elif args['get_post']:
        TargetSpider.test_get_post()
    elif args['all']:
        TargetSpider.test_all()


if __name__ == "__main__":
    args = docopt(__doc__)
    test_spider(args)
