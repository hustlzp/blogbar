# coding: utf-8
from flask import render_template, Blueprint, flash, redirect, url_for
from ..models import db, Blog
from ..forms import BlogForm
from ..utils.blog import grab_blog

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
        if blog.feed:
            try:
                grab_blog(blog)
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
