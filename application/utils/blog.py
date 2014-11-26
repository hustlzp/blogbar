# coding: utf-8
from lxml import html
import feedparser
import HTMLParser
from time import mktime
from datetime import datetime
from ..models import db, Post


def grab_by_feed(blog):
    new_posts_count = 0

    result = feedparser.parse(blog.feed)
    if not blog.feed_version:
        blog.feed_version = result.version
    if not blog.subtitle and 'subtitle' in result.feed:
        blog.subtitle = get_text_from_html(result.feed.subtitle)

    db.session.add(blog)
    print(blog.title)

    for entry in result.entries:
        url = entry.link
        post = blog.posts.filter(Post.url == url).first()
        # 新博文
        if not post:
            new_posts_count += 1
            post = Post(url=url)
            _get_info_to_post(post, entry)
            blog.posts.append(post)
            print(" new - %s" % post.title)
        else:
            # 更新
            updated_at = None
            published_at = None

            if 'updated_parsed' in entry:
                updated_at = _get_time(entry.updated_parsed)
            if 'published_parsed' in entry:
                published_at = _get_time(entry.published_parsed)

            if (updated_at and updated_at != post.updated_at) or (
                        published_at and published_at != post.published_at):
                _get_info_to_post(post, entry)
                print(" update - %s" % post.title)
                db.session.add(post)
    db.session.commit()
    return new_posts_count


def _get_info_to_post(post, entry):
    """将entry中的信息转存到post中"""
    title = get_text_from_html(entry.title)  # 去除HTML标签
    title = title.replace('\r', '').replace('\n', '')  # 去除换行符
    html_parser = HTMLParser.HTMLParser()
    post.title = html_parser.unescape(title)  # HTML反转义
    post.url = entry.link

    if 'published_parsed' in entry:
        post.published_at = _get_time(entry.published_parsed)
    if 'updated_parsed' in entry:
        post.updated_at = _get_time(entry.updated_parsed)

    # 若published_at不存在，则使用updated_at
    if not post.published_at:
        post.published_at = post.updated_at

    if 'content' in entry:
        if isinstance(entry.content, list):
            post.content = entry.content[0].value
        else:
            post.content = entry.content
    elif 'summary' in entry:
        post.content = entry.summary
    post.update()


def _get_time(time_struct):
    return datetime.fromtimestamp(mktime(time_struct))


def get_text_from_html(html_string):
    doc = html.fromstring(html_string)  # parse html string
    return doc.text_content()
