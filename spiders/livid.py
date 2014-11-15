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
        for a in tree.cssselect('.posts a'):
            posts.append({
                'url': a.get('href'),
                'title': a.text_content()
            })
        return posts

    @staticmethod
    def get_post(tree, url):
        date_element = tree.cssselect('div.date')[0]
        published_at = datetime.strptime(date_element.text_content(), "%d %B %Y")

        content_element = tree.cssselect('div.span10')[0]
        content = get_inner_html(content_element)

        return {
            'published_at': published_at,
            'content': content
        }
