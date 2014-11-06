# coding: utf-8
import feedparser
from time import mktime
from datetime import datetime
from ..models import db, Post


def grab_blog(blog):
    result = feedparser.parse(blog.feed)
    if 'updated_parsed' in result.feed:
        blog.updated_at = _get_time(result.feed.updated_parsed)
    if 'id' in result.feed:
        blog.unique_id = result.feed.id
    elif 'link' in result.feed:
        blog.unique_id = result.feed.link
    blog.feed_version = result.version
    if 'subtitle' in result.feed:
        blog.subtitle = result.feed.subtitle

    db.session.add(blog)
    print(blog.title)

    # 最新博文
    for entry in result.entries:
        identity = entry.id if 'id' in entry else entry.link
        post = blog.posts.filter(Post.unique_id == identity).first()
        if not post:
            post = Post(title=entry.title, url=entry.link, unique_id=identity)
            if 'updated_parsed' in entry:
                post.updated_at = _get_time(entry.updated_parsed)
            if 'published_parsed' in entry:
                post.published_at = _get_time(entry.published_parsed)

            if 'content' in entry:
                if isinstance(entry.content, list):
                    post.content = entry.content[0].value
                else:
                    post.content = entry.content
            elif 'summary' in entry:
                post.content = entry.summary
            blog.posts.append(post)
            print(" new - %s" % post.title)
        else:
            if 'updated_parsed' in entry:
                post.updated_at = _get_time(entry.updated_parsed)
            if 'published_parsed' in entry:
                post.published_at = _get_time(entry.published_parsed)
            print(" update - %s" % post.title)
            db.session.add(post)
    db.session.commit()


def _get_time(time_struct):
    return datetime.fromtimestamp(mktime(time_struct))