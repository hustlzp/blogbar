# coding: utf-8
import datetime
from .base import BaseSpider, get_inner_html, remove_element


class YourSpider(BaseSpider):
    url = ""
    posts_url = ""  # 按需添加
    title = ""
    subtitle = ""
    author = ""

    @staticmethod
    def get_posts(tree):
        pass

    @staticmethod
    def get_post(tree):
        pass
