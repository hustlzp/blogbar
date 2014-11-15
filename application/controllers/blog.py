# coding: utf-8
from flask import render_template, Blueprint, flash, redirect, url_for, abort, request
from werkzeug.contrib.atom import AtomFeed, FeedEntry
from ..models import db, Blog, Post
from ..forms import BlogForm
from ..utils.blog import grab_by_feed

bp = Blueprint('blog', __name__)


@bp.route('/<int:uid>')
def view(uid):
    blog = Blog.query.get_or_404(uid)
    return render_template('blog/view.html', blog=blog)


@bp.route('/add', methods=['GET', 'POST'])
def add():
    """添加博客"""
    form = BlogForm()
    if form.validate_on_submit():
        blog = Blog(**form.data)
        blog.url = blog.url.rstrip('/')
        if blog.feed:
            try:
                grab_by_feed(blog)
            except Exception, e:
                print(e)
                blog.last_status = False
                flash('Feed抓取失败')
            else:
                blog.last_status = True
                flash('Feed抓取成功，共抓取 %d 篇日志' % blog.posts.count())
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for('site.index'))
    return render_template('blog/add.html', form=form)


@bp.route('/post/<int:uid>')
def post(uid):
    post = Post.query.get_or_404(uid)
    return render_template('blog/post.html', post=post)


@bp.route('/<int:uid>/feed')
def feed(uid):
    blog = Blog.query.get_or_404(uid)
    if blog.feed:
        abort(404)
    feed = AtomFeed(blog.title, feed_url=request.url, url=blog.url, id=blog.url)
    if blog.subtitle:
        feed.subtitle = blog.subtitle
    for post in blog.posts.order_by(Post.published_at.desc()).limit(15):
        updated = post.updated_at if post.updated_at else post.published_at
        entry = FeedEntry(post.title, post.content, content_type='html', author=blog.author,
                          url=post.url, id=post.url, updated=updated)
        feed.add(entry)
    response = feed.get_response()
    response.headers['Content-Type'] = 'application/xml'
    return response