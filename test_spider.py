# coding: utf-8


def test_spider():
    """测试Spider

    将下方的LividSpider替换为你写的SPider，
    然后运行python manage.py test_spider即可。

    共有3条测试指令：
        1. test_get_posts: 测试get_posts
        2. test_get_post: 测试get_post
        3. test_format: 测试全部数据的格式

    建议按顺序依次测试：
        运行1（注释2、3），观察输出是否正常
        运行2（注释1、3），观察输出是否正常
        运行3（注释1、2），观察是否通过格式测试
    """
    from spiders import LividSpider as TargetSpider

    TargetSpider.test_get_posts()  # 测试get_posts
    TargetSpider.test_get_post()  # 测试get_post
    TargetSpider.test_format()  # 测试全部数据的格式


if __name__ == "__main__":
    test_spider()