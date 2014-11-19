# coding: utf-8
import pprint
import HTMLParser
import requests
from urlparse import urlparse
from lxml import html, etree
from datetime import datetime


class MyPrettyPrinter(pprint.PrettyPrinter):
    """支持中文输出的pprint"""

    def format(self, obj, context, maxlevels, level):
        if isinstance(obj, unicode):
            return obj.encode('utf8'), True, False
        return pprint.PrettyPrinter.format(self, obj, context, maxlevels, level)


pp = MyPrettyPrinter(indent=2)


class BaseSpider(object):
    url = ""  # 网址
    posts_url = ""  # 包含博文列表的网址
    title = ""  # 博客标题
    subtitle = ""  # 博客副标题
    author = ""  # 博主

    @classmethod
    def get_posts_(cls):
        """获取post列表

        返回格式
            [
                {'url': '', 'title': '', 'published_at': ''},
                {'url': '', 'title': '', 'published_at': ''},
                {'url': '', 'title': '', 'published_at': ''}
            ]
        """
        tree = _get_tree(cls.posts_url or cls.url)
        posts = cls.get_posts(tree)
        html_parser = HTMLParser.HTMLParser()
        for p in posts:
            p['title'] = html_parser.unescape(p['title'])
        return posts

    @staticmethod
    def get_posts(tree):
        """根据tree，获取post列表。

        子类必须重载此方法。

        返回格式
            [
                {'url': '', 'title': '', 'published_at': ''},
                {'url': '', 'title': '', 'published_at': ''},
                {'url': '', 'title': '', 'published_at': ''}
            ]
        """
        raise NotImplementedError()

    @classmethod
    def get_post_(cls, url):
        """根据url，获取post内容

        返回格式
            content
        """
        html_parser = HTMLParser.HTMLParser()
        tree = _get_tree(url)

        # 去除script
        scripts = tree.cssselect('script')
        map(remove_element, scripts)

        # 去除style
        styles = tree.cssselect('style')
        map(remove_element, styles)

        content = cls.get_post(tree)
        return html_parser.unescape(content)  # HTML解码

    @staticmethod
    def get_post(tree):
        """根据tree，获取post内容。

        子类必须重载此方法。

        返回格式
            content
        """
        raise NotImplementedError()

    @classmethod
    def test_get_posts(cls):
        """测试get_posts"""
        posts = cls.get_posts_()
        pp.pprint(posts)

    @classmethod
    def test_get_post(cls):
        """测试get_post"""
        posts = cls.get_posts_()
        url = posts[0]['url']
        content = cls.get_post_(url)
        pp.pprint(content)

    @classmethod
    def test_all(cls):
        """测试所有返回数据的格式"""
        posts = cls.get_posts_()
        assert isinstance(posts, list)

        for post in posts:
            assert isinstance(post, dict)
            assert 'url' in post and post['url']
            assert 'title' in post and post['title']
            assert 'published_at' in post \
                   and isinstance(post['published_at'], datetime)
            content = cls.get_post_(post['url'])
            assert content
            print("%s - ok" % post['title'])
        print('-------------------------------------')
        print('All passed!')


def get_inner_html(element):
    """获取element中的HTML内容"""
    content_list = [element.text or ''] \
                   + [etree.tostring(child) for child in element]
    html = ''.join(content_list).strip()
    html_parser = HTMLParser.HTMLParser()
    return html_parser.unescape(html)


def remove_element(element):
    """去除此元素"""
    parent = element.getparent()
    parent.remove(element)


def _get_tree(url):
    """根据url获取ElementTree"""
    page = requests.get(url)
    tree = html.fromstring(page.text)
    host = _get_host(url)
    tree.make_links_absolute(host)
    return tree


def _get_host(url):
    """获取url中的host"""
    parsed_uri = urlparse(url)
    return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
