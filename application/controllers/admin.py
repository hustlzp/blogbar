# coding: utf-8
import json
import datetime
from flask import render_template, Blueprint, flash, redirect, url_for, abort, request
from ..models import db, Blog, Post, ApprovementLog, Kind, BlogKind
from ..utils.permissions import AdminPermission
from ..forms import EditBlogForm

bp = Blueprint('admin', __name__)


@bp.route('/approve', defaults={'page': 1})
@bp.route('/approve/page/<int:page>')
@AdminPermission()
def approve(page):
    """审核博客"""
    logs = ApprovementLog.query
    unprocessed_logs = logs.filter(ApprovementLog.status == -1).order_by(
        ApprovementLog.updated_at.desc())
    processed_logs = logs.filter(ApprovementLog.status != -1).order_by(
        ApprovementLog.status.desc(),
        ApprovementLog.updated_at.desc()).paginate(page, 20)
    return render_template('admin/approve.html', unprocessed_logs=unprocessed_logs,
                           processed_logs=processed_logs)


@bp.route('/approve_blog/<int:uid>', methods=['POST'])
@AdminPermission()
def approve_blog(uid):
    """通过审核"""
    blog = Blog.query.get_or_404(uid)
    is_approved = True if 'yes' in request.form else False
    # 更新blog
    blog.is_approved = is_approved
    db.session.add(blog)
    # 更新log
    log = ApprovementLog.query.filter(ApprovementLog.blog_id == uid).first_or_404()
    log.updated_at = datetime.datetime.now()
    log.status = 1 if is_approved else 0
    log.message = request.form.get('message')
    db.session.add(log)
    db.session.commit()
    flash('操作成功')
    return redirect(request.referrer)


@bp.route('/edit_blog/<int:uid>', methods=['GET', 'POST'])
@AdminPermission()
def edit_blog(uid):
    """编辑博客"""
    blog = Blog.query.get_or_404(uid)
    form = EditBlogForm(obj=blog)
    kinds = Kind.query.order_by(Kind.show_order.asc())
    blog_kinds = [blog_kind.kind_id for blog_kind in blog.blog_kinds]
    if form.validate_on_submit():
        form.populate_obj(blog)
        db.session.add(blog)
        db.session.commit()
        flash('操作成功')
        return redirect(request.form.get('referer') or request.referrer or url_for('site.idnex'))
    return render_template('admin/edit_blog.html', form=form, kinds=kinds, blog_kinds=blog_kinds,
                           blog=blog)


@bp.route('/delete_blog/<int:uid>')
@AdminPermission()
def delete_blog(uid):
    """删除博客"""
    blog = Blog.query.get_or_404(uid)
    db.session.delete(blog)
    db.session.commit()
    flash('已删除')
    return redirect(url_for('site.index'))


@bp.route('/blogs')
@AdminPermission()
def blogs():
    offline_blogs = Blog.query.filter(Blog.offline)
    bad_feed_blogs = Blog.query.filter(Blog.bad_feed)
    return render_template('admin/blogs.html', offline_blogs=offline_blogs,
                           bad_feed_blogs=bad_feed_blogs)


@bp.route('/posts', defaults={'page': 1})
@bp.route('/posts/page/<int:page>')
@AdminPermission()
def posts(page):
    """管理文章"""
    posts = Post.query.order_by(Post.published_at.desc()).paginate(page, 20)
    return render_template('admin/posts.html', posts=posts)


@bp.route('/recommend_post/<int:uid>')
@AdminPermission()
def recommend_post(uid):
    """推荐文章"""
    post = Post.query.get_or_404(uid)
    post.recommend = True
    db.session.add(post)
    db.session.commit()
    return redirect(request.referrer)


@bp.route('/unrecommend_post/<int:uid>')
@AdminPermission()
def unrecommend_post(uid):
    """取消推荐文章"""
    post = Post.query.get_or_404(uid)
    post.recommend = False
    db.session.add(post)
    db.session.commit()
    return redirect(request.referrer)


@bp.route('/hide_post/<int:uid>')
@AdminPermission()
def hide_post(uid):
    """隐藏文章"""
    post = Post.query.get_or_404(uid)
    post.hide = True
    db.session.add(post)
    db.session.commit()
    return redirect(request.referrer)


@bp.route('/show_post/<int:uid>')
@AdminPermission()
def show_post(uid):
    """显示文章"""
    post = Post.query.get_or_404(uid)
    post.hide = False
    db.session.add(post)
    db.session.commit()
    return redirect(request.referrer)


@bp.route('/add_kind_to_blog', methods=['POST'])
@AdminPermission()
def add_kind_to_blog():
    kind_id = request.form.get('kind_id', type=int)
    blog_id = request.form.get('blog_id', type=int)
    if not kind_id or not blog_id:
        abort(500)
    if not BlogKind.query.filter(BlogKind.blog_id == blog_id,
                                 BlogKind.kind_id == kind_id).first():
        blog = Blog.query.get_or_404(blog_id)
        kind = Kind.query.get_or_404(kind_id)
        blog_kind = BlogKind(blog_id=blog_id, kind_id=kind_id)
        db.session.add(blog_kind)
        db.session.commit()
    return json.dumps({'status': 'yes'})


@bp.route('/remove_kind_from_blog', methods=['POST'])
@AdminPermission()
def remove_kind_from_blog():
    kind_id = request.form.get('kind_id', type=int)
    blog_id = request.form.get('blog_id', type=int)
    if not kind_id or not blog_id:
        abort(500)
    blog_kinds = BlogKind.query.filter(BlogKind.blog_id == blog_id,
                                       BlogKind.kind_id == kind_id)
    map(db.session.delete, blog_kinds)
    db.session.commit()
    return json.dumps({'status': 'yes'})
