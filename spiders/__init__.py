from .lifesinger import LifeSingerSpider
from .wangyin import WangYinSpider
from .application import create_app
from .application.models import db, Blog, Post

subclasses = [
    LifeSingerSpider,
    WangYinSpider
]

app = create_app()


def grab(spider_class):
    new_posts_count = 0

    with app.app_context():
        blog = Blog.query.filter(Blog.unique_id == spider_class.url).first_or_404()
        for post in spider_class.get_posts_():
            url = post['url']
            title = post['title']
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
        db.session.add(blog)
        db.session.commit()
        return new_posts_count