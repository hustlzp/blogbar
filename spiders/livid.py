# coding: utf-8
from .base import BaseSpider, get_inner_html
from datetime import datetime


class LividSpider(BaseSpider):
    url = "http://livid.v2ex.com"
    title = "Livid"
    author = "Livid"

    @staticmethod
    def get_posts(tree):
        posts = []
        for li in tree.cssselect('.posts li'):
            date_element = li.cssselect('span')[0]
            published_at = datetime.strptime(date_element.text_content(), "%d %b %Y")
            link = li.cssselect('a')[0]
            posts.append({
                'url': link.get('href'),
                'title': link.text_content(),
                'published_at': published_at
            })
        return posts

    @staticmethod
    def get_post(tree):
        content_element = tree.cssselect('div.span10')[0]
        return get_inner_html(content_element)
