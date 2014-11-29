# coding: utf-8
import requests
import feedparser
from HTMLParser import HTMLParser
from time import mktime
from datetime import datetime
from datetime import timedelta
from ..models import db, Post


def grab_by_feed(blog):
    new_posts_count = 0

    # 检测博客是否在线
    try:
        res = requests.get(blog.url)
        if res.status_code >= 400:
            blog.offline = True
    except Exception, e:
        blog.offline = True

    result = feedparser.parse(blog.feed)

    # feed失效
    if not result.feed:
        blog.bad_feed = True
    if not blog.feed_version:
        blog.feed_version = result.version
    if not blog.subtitle and 'subtitle' in result.feed:
        blog.subtitle = remove_html_tag(result.feed.subtitle)

    db.session.add(blog)
    print(blog.title)

    timezone_offset = blog.feed_timezone_offset

    for entry in result.entries:
        url = entry.link
        post = blog.posts.filter(Post.url == url).first()
        # 新博文
        if not post:
            new_posts_count += 1
            post = Post(url=url)
            _get_info_to_post(post, entry, timezone_offset)
            blog.posts.append(post, blog)
            print(" new - %s" % post.title)
        else:
            # 更新
            updated_at = None
            published_at = None

            if 'updated_parsed' in entry:
                updated_at = _get_time(entry.updated_parsed, timezone_offset)
            if 'published_parsed' in entry:
                published_at = _get_time(entry.published_parsed, timezone_offset)

            if (updated_at and updated_at != post.updated_at) or (
                        published_at and published_at != post.published_at):
                _get_info_to_post(post, entry, timezone_offset)
                print(" update - %s" % post.title)
                db.session.add(post)
    db.session.commit()
    return new_posts_count


def _get_info_to_post(post, entry, timezone_offset):
    """将entry中的信息转存到post中"""
    title = remove_html_tag(entry.title)  # 去除HTML标签
    title = title.replace('\r', '').replace('\n', '')  # 去除换行符
    html_parser = HTMLParser()
    post.title = html_parser.unescape(title)  # HTML反转义
    post.url = entry.link

    if 'published_parsed' in entry:
        post.published_at = _get_time(entry.published_parsed, timezone_offset)
    if 'updated_parsed' in entry:
        post.updated_at = _get_time(entry.updated_parsed, timezone_offset)

    # 若published_at不存在，则使用updated_at
    if not post.published_at and post.updated_at:
        post.published_at = post.updated_at

    # 若published_at与updated_at均不存在，则使用当前时间作为publishe_at
    if not post.published_at and not post.updated_at:
        post.publishe_at = datetime.now()

    if 'content' in entry:
        if isinstance(entry.content, list):
            post.content = entry.content[0].value
        else:
            post.content = entry.content
    elif 'summary' in entry:
        post.content = entry.summary


def _get_time(time_struct, timezone_offset=None):
    result_time = datetime.fromtimestamp(mktime(time_struct))
    if timezone_offset:
        result_time -= timedelta(hours=timezone_offset)
    return result_time


# See: http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def remove_html_tag(html_string):
    s = MLStripper()
    s.feed(html_string)
    return s.get_data()
