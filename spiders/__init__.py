# coding: utf-8
from .base import get_inner_html
from .lifesinger import LifeSingerSpider
from .wangyin import WangYinSpider
from .livid import LividSpider
from application.models import db, Blog, Post

spiders = [
    LifeSingerSpider,
    WangYinSpider,
    LividSpider
]


def grab_by_spider(spider_class):
    new_posts_count = 0

    blog = Blog.query.filter(Blog.url == spider_class.url).first()

    # 若不存在，则创建
    if not blog:
        blog = Blog(url=spider_class.url, title=spider_class.title,
                    subtitle=spider_class.subtitle, author=spider_class.author)
        db.session.add(blog)
        db.session.commit()

    for p in spider_class.get_posts_():
        url = p['url']
        title = p['title']

        post = Post.query.filter(Post.url == url).first()
        post_info = spider_class.get_post_(url)

        # 新文章
        if not post:
            new_posts_count += 1
            post = Post(url=url, title=title, content=post_info['content'])
            if 'published_at' in post_info:
                post.published_at = post_info['published_at']
            if 'updated_at' in post_info:
                post.updated_at = post_info['updated_at']
            blog.posts.append(post)
            print(" new - %s" % title)
        else:  # 更新文章
            published_at = post_info.get('published_at')
            updated_at = post_info.get('updated_at')

            if (published_at and published_at != post.published_at) \
                    or (updated_at and updated_at != post.updated_at):
                if published_at:
                    post.published_at = published_at
                if updated_at:
                    post.updated_at = updated_at
                post.title = title
                post.content = post_info['content']
                db.session.add(post)
                print(" update - %s" % title)
    db.session.add(blog)
    db.session.commit()
    return new_posts_count