# coding: utf-8
import HTMLParser
import requests
from lxml import html, etree


class BaseSpider(object):
    url = ""
    title = ""
    subtitle = ""
    author = ""

    @classmethod
    def get_posts_(cls):
        """获取post列表

        返回格式
            [{'url':'', 'title': ''}]
        """
        tree = cls.get_tree(cls.url)
        host = cls.get_host(cls.url)
        tree.make_links_absolute(host)
        return cls.get_posts(tree)

    @staticmethod
    def get_posts(tree):
        """根据tree，获取post列表

        返回格式
            [{'url':'', 'title': ''}]
        """
        raise NotImplementedError()

    @classmethod
    def get_post_(cls, url):
        """根据url，获取post信息

        返回格式
            {content: '', published_at: '', updated_at: ''}
        """
        html_parser = HTMLParser.HTMLParser()
        tree = cls.get_tree(url)
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
    def get_tree(url):
        """根据url获取ElementTree"""
        page = requests.get(url)
        return html.fromstring(page.text)

    @staticmethod
    def get_host(url):
        from urlparse import urlparse

        parsed_uri = urlparse(url)
        return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

    @staticmethod
    def get_inner_html(element):
        content_list = [element.text or ''] \
                       + [etree.tostring(child) for child in element]
        html = ''.join(content_list).strip()
        html_parser = HTMLParser.HTMLParser()
        return html_parser.unescape(html)