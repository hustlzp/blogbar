# coding: utf-8
import datetime
from .base import BaseSpider, get_inner_html, remove_element


class WangYinSpider(BaseSpider):
    url = 'http://www.yinwang.org'
    title = '当然我在扯淡'
    author = '王垠'

    @staticmethod
    def get_posts(tree):
        posts = []
        for item in tree.cssselect('.list-group-item a'):
            title = item.text_content()
            url = item.get('href')
            # 获取日期
            date_list = filter(None, url.split('/'))
            day = int(date_list[-2])
            month = int(date_list[-3])
            year = int(date_list[-4])
            published_at = datetime.datetime(year=year, month=month, day=day)
            posts.append({
                'title': title,
                'url': url,
                'published_at': published_at
            })
        return posts

    @staticmethod
    def get_post(tree):
        content_element = tree.cssselect('body')[0]
        remove_element(content_element.cssselect('h2')[0])  # 去除h2标题
        remove_element(content_element.cssselect('p')[0])  # 去除第一个段落
        return get_inner_html(content_element)
