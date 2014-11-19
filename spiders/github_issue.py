# coding: utf-8
import datetime
from .base import BaseSpider, get_inner_html


class GitHubIssueSpider(BaseSpider):
    @staticmethod
    def get_posts(tree):
        posts = []
        for item in tree.cssselect('.table-list-item'):
            title_element = item.cssselect('.issue-title-link')[0]
            title = title_element.text_content().strip()
            url = title_element.get('href')
            # 发表日期
            date_text = item.cssselect('time')[0].get('datetime')
            published_at = datetime.datetime.strptime(date_text, '%Y-%m-%dT%H:%M:%SZ')
            posts.append({
                'url': url,
                'title': title,
                'published_at': published_at
            })
        return posts

    @staticmethod
    def get_post(tree):
        content_element = tree.cssselect('.comment-body')[0]
        return get_inner_html(content_element)