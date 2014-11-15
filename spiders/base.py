# coding: utf-8
import HTMLParser
import requests
from lxml import html, etree
from datetime import datetime


class BaseSpider(object):
    url = ""  # 网址
    title = ""  # 博客标题
    subtitle = ""  # 博客副标题
    author = ""  # 博主

    @classmethod
    def get_posts_(cls):
        """获取post列表

        返回格式
            [
                {'url': '', 'title': ''},
                {'url': '', 'title': ''},
                {'url': '', 'title': ''}
            ]
        """
        tree = cls._get_tree(cls.url)
        host = cls._get_host(cls.url)
        tree.make_links_absolute(host)
        return cls.get_posts(tree)

    @staticmethod
    def get_posts(tree):
        """根据tree，获取post列表

        返回格式
            [
                {'url': '', 'title': ''},
                {'url': '', 'title': ''},
                {'url': '', 'title': ''}
            ]
        """
        raise NotImplementedError()

    @classmethod
    def get_post_(cls, url):
        """根据url，获取post信息

        返回格式
            {content: '', published_at: '', updated_at: ''}
        """
        html_parser = HTMLParser.HTMLParser()
        tree = cls._get_tree(url)
        post_info = cls.get_post(tree, url)
        post_info['content'] = html_parser.unescape(post_info['content'])
        return post_info

    @staticmethod
    def get_post(tree, url):
        """根据tree，获取post信息

        返回格式
            {content: '', published_at: '', updated_at: ''}
        """
        raise NotImplementedError()

    @staticmethod
    def get_inner_html(element):
        """获取element中的HTML内容"""
        content_list = [element.text or ''] \
                       + [etree.tostring(child) for child in element]
        html = ''.join(content_list).strip()
        html_parser = HTMLParser.HTMLParser()
        return html_parser.unescape(html)

    @classmethod
    def test(cls):
        """测试返回格式"""
        posts = cls.get_posts_()
        assert isinstance(posts, list)

        for post in posts:
            assert isinstance(post, dict)
            assert 'url' in post and post['url']
            assert 'title' in post and post['title']

            post_info = cls.get_post_(post['url'])
            assert isinstance(post_info, dict)
            assert 'content' in post_info and post_info['content']
            assert ('published_at' in post_info
                    and isinstance(post_info['published_at'], datetime)) \
                   or ('updated_at' in post_info
                       and isinstance(post_info['updated_at'], datetime))
            print("%s - pass" % post['title'])

    @staticmethod
    def _get_tree(url):
        """根据url获取ElementTree"""
        page = requests.get(url)
        return html.fromstring(page.text)

    @staticmethod
    def _get_host(url):
        """获取url中的host"""
        from urlparse import urlparse

        parsed_uri = urlparse(url)
        return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)