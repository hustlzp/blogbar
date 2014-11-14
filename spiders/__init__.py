# coding: utf-8
from .lifesinger import LifeSingerSpider
from .wangyin import WangYinSpider
from .application import create_app
from .application.models import db, Blog, Post

subclasses = [
    LifeSingerSpider,
    WangYinSpider
]


def grab_by_spider(spider_class):
    new_posts_count = 0
    app = create_app()

    with app.app_context():
        blog = Blog.query.filter(Blog.unique_id == spider_class.url).first()

        for p in spider_class.get_posts_():
            url = p['url']
            title = p['title']
            print(title)

            post = Post.query.filter(Post.unique_id == url).first()

            # 新文章
            if not post:
                new_posts_count += 1
                post_info = spider_class.get_post_(url)
                post = Post(url=url, unique_id=url, title=title, content=post_info['content'])
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