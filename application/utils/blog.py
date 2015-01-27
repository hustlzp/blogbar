# coding: utf-8
import re
import socket
import requests
import feedparser
import logging
from HTMLParser import HTMLParser
from flask import current_app
from time import mktime
from datetime import datetime, timedelta
from ..models import db, Post, FEED_STATUS_GOOD, FEED_STATUS_BAD, FEED_STATUS_TIMEOUT
from .helper import Timeout, remove_html


def grab_by_feed(blog):
    """通过Feed获取博客内容"""
    new_posts_count = 0

    # logging.debug(blog.title)
    print(blog.title)

    # 检测博客是否在线
    blog.offline = check_offline(blog.url)

    # 读取feed，20s超时
    # try:
    # with Timeout(20):
    result = parse_feed(blog.feed, 30)
    # except Timeout.Timeout:
    #     blog.feed_status = FEED_STATUS_TIMEOUT
    #     print(' feed timeout')
    # else:
    if not result.entries:
        if hasattr(result, 'bozo_exception') and isinstance(result.bozo_exception, socket.timeout):
            blog.feed_status = FEED_STATUS_TIMEOUT
        else:
            blog.feed_status = FEED_STATUS_BAD
    else:
        blog.feed_status = FEED_STATUS_GOOD

    # 若feed无效，则退出
    if blog.feed_status != FEED_STATUS_GOOD:
        db.session.add(blog)
        db.session.commit()
        return 0

    # 更新博客信息
    if not blog.feed_version:
        blog.feed_version = result.version
    if not blog.subtitle and 'subtitle' in result.feed:
        blog.subtitle = _process_title(result.feed.subtitle)

    timezone_offset = blog.feed_timezone_offset or 0

    # 用于计算blog最后更新时间
    last_updated_at = datetime.min

    for entry in result.entries:
        entry.link = _uniform_url(entry.link)
        exist, post = _check_entry_exist(entry, blog)

        if exist:
            # 更新文章
            _get_info_to_post(post, entry, timezone_offset)
            db.session.add(post)
        else:
            # 新博文
            post = Post()
            _get_info_to_post(post, entry, timezone_offset)
            blog.posts.append(post)
            new_posts_count += 1
            # logging.debug(" new - %s" % post.title)
            print(" new - %s" % post.title)

        if post.published_at > last_updated_at:
            last_updated_at = post.published_at

    blog.updated_at = last_updated_at
    db.session.add(blog)
    db.session.commit()
    return new_posts_count


def _check_entry_exist(entry, blog):
    """判断该entry是否存在于该博客中"""
    exist = False
    timezone_offset = blog.feed_timezone_offset or 0
    post = blog.posts.filter(Post.url == entry.link).first()
    if post:
        exist = True
    else:
        # 是否存在标题一致，且发表时间相近的文章
        post = blog.posts.filter(Post.title == _process_title(entry.title)).first()
        if post:
            published_at = _get_entry_published_at(entry, timezone_offset)
            if published_at:
                exist = _get_time_diff(published_at, post.published_at) <= timedelta(days=1)
            else:
                exist = True
        else:
            # 是否存在标题一致，且发表时间相近的文章
            entry_content = _get_entry_content(entry)
            post = blog.posts.filter(Post.content == entry_content).first()
            if post:
                published_at = _get_entry_published_at(entry, timezone_offset)
                if published_at:
                    exist = _get_time_diff(published_at, post.published_at) <= timedelta(days=1)
                else:
                    exist = True
    return exist, post


def _uniform_url(url):
    """补全scheme"""
    from urlparse import urlparse

    parse_result = urlparse(url)
    if parse_result.scheme == "":
        url = "http://%s" % url
    return url


def _get_time_diff(one_time, another_time):
    """计算时间差"""
    if one_time >= another_time:
        timediff = one_time - another_time
    else:
        timediff = another_time - one_time
    return timediff


def _get_info_to_post(post, entry, timezone_offset):
    """将entry中的信息转存到post中"""
    post.title = _process_title(entry.title)
    post.url = entry.link

    if 'published_parsed' in entry:
        post.published_at = _get_time(entry.published_parsed, timezone_offset)
    if 'updated_parsed' in entry:
        post.updated_at = _get_time(entry.updated_parsed, timezone_offset)

    # 若published_at不存在，则使用updated_at
    if not post.published_at and post.updated_at:
        post.published_at = post.updated_at

    # 若published_at与updated_at均不存在，则使用当前时间作为published_at
    config = current_app.config
    timezone = config.get('TIMEZONE')
    if not post.published_at and not post.updated_at:
        post.published_at = datetime.now() - timedelta(hours=timezone)

    post.content = _get_entry_content(entry)


def _get_entry_content(entry):
    """获取entry中的文章正文"""
    content = ''
    if 'content' in entry:
        if isinstance(entry.content, list):
            content = entry.content[0].value
        else:
            content = entry.content
    elif 'summary' in entry:
        content = entry.summary
    return content


def _process_title(title):
    """处理feed.entries中的title"""
    html_parser = HTMLParser()
    title = html_parser.unescape(title)  # 进行2次HTML反转义
    title = html_parser.unescape(title)
    title = title.replace('\r', '').replace('\n', '')  # 去除换行符
    return remove_html(title)


def _get_entry_published_at(entry, timezone_offset):
    """获取entry中的published_at"""
    if 'published_parsed' in entry:
        return _get_time(entry.published_parsed, timezone_offset)
    elif 'updated_parsed' in entry:
        return _get_time(entry.updated_parsed, timezone_offset)
    else:
        return None


def _get_time(time_struct, timezone_offset=None):
    """获取UTC时间"""
    result_time = datetime.fromtimestamp(mktime(time_struct))
    if timezone_offset:
        result_time -= timedelta(hours=timezone_offset)
    return result_time


def check_offline(url):
    """判断博客是否在线。"""
    try:
        res = requests.get(url, verify=False)
        if (res.status_code >= 500
            or res.status_code == 404
            or 'http://mcc.godaddy.com/park' in res.text
            or 'Welcome to nginx!' in res.text
            or '<h1>It works!</h1>' in res.text
            or not res.text):
            return True
        else:
            return False
    except Exception, e:
        return True


def parse_feed(feed, timeout=None):
    """解析Feed"""
    if timeout:
        socket.setdefaulttimeout(timeout)

    # 解析Feed时设置User-Agent和Referer头部，以免出现403现象
    config = current_app.config
    site_domain = config.get('SITE_DOMAIN')
    result = feedparser.parse(feed, agent=site_domain, referrer=site_domain)

    # 天涯博客
    if 'blog.tianya.cn' in feed:
        for entry in result.entries:
            published_text = entry.published.split('(')[0]
            published = datetime.strptime(published_text, "%Y-%m-%d %H:%M:%S")
            entry.published_parsed = published.timetuple()

    socket.setdefaulttimeout(None)
    return result


def forbidden_url(url):
    """禁止某些URL"""
    return re.compile("fuck|porn|sex|adult|dating|swinger|xxx|xvideo", re.I).search(url)
