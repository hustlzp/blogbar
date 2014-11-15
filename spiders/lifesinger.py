# coding: utf-8
import datetime
from .base import BaseSpider, get_inner_html


class LifeSingerSpider(BaseSpider):
    url = 'https://github.com/lifesinger/lifesinger.github.com/issues?q=label:blog'
    title = '岁月如歌'
    author = '玉伯'

    @staticmethod
    def get_posts(tree):
        posts = []
        for item in tree.cssselect('.table-list-item'):
            title_element = item.cssselect('.issue-title-link')[0]
            title = title_element.text_content().strip()
            url = title_element.get('href')
            posts.append({
                'url': url,
                'title': title
            })
        return posts

    @staticmethod
    def get_post(tree, url):
        # 获取发表日期
        date_text = tree.cssselect('.gh-header-meta time')[0].get('datetime')
        published_at = datetime.datetime.strptime(date_text, '%Y-%m-%dT%H:%M:%SZ')

        # 获取内容
        content_element = tree.cssselect('.comment-body')[0]
        content = get_inner_html(content_element)

        return {
            'published_at': published_at,
            'content': content
        }
