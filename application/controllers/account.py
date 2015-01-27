# coding: utf-8
import datetime
from flask import render_template, Blueprint, redirect, request, url_for, g, flash
from ..forms import SigninForm, SignupForm
from ..utils.account import signin_user, signout_user
from ..utils.permissions import VisitorPermission, UserPermission
from ..utils.mail import send_active_mail
from ..models import db, User, Post, Blog

bp = Blueprint('account', __name__)


@bp.route('/signin', methods=['GET', 'POST'])
@VisitorPermission()
def signin():
    """登陆"""
    form = SigninForm()
    if form.validate_on_submit():
        signin_user(form.user)
        return redirect(url_for('site.index'))
    return render_template('account/signin.html', form=form)


@bp.route('/signup', methods=['GET', 'POST'])
@VisitorPermission()
def signup():
    """Signup"""
    form = SignupForm()
    if form.validate_on_submit():
        params = form.data.copy()
        params.pop('repassword')
        user = User(**params)
        db.session.add(user)
        db.session.commit()
        if send_active_mail(user):
            messages = ['激活链接已发送到你的邮箱，请查收。']
        else:
            messages = ['激活链接发送失败。']
        return render_template('account/tip.html', messages=messages)
    return render_template('account/signup.html', form=form)


@bp.route('/signout')
def signout():
    """登出"""
    signout_user()
    return redirect(request.referrer or url_for('site.index'))


@bp.route('/active')
@VisitorPermission()
def active():
    """激活账户"""
    user_id = request.args.get('user_id', type=int)
    token = request.args.get('token')

    if not user_id or not token:
        flash('激活失败')
        return redirect(url_for('site.index'))

    user = User.query.filter(User.id == user_id, User.token == token).first()
    if not user:
        flash('激活失败')
        return redirect(url_for('site.index'))

    if user.is_active:
        return redirect(url_for('site.index'))

    user.is_active = True
    user.update_token()
    db.session.add(user)
    db.session.commit()

    signin_user(user)
    flash('激活成功，欢迎来到 Blogbar')
    return redirect(url_for('site.index'))


@bp.route('/subscription', defaults={'page': 1})
@bp.route('/subscription/page/<int:page>')
@UserPermission()
def subscription(page):
    """我的订阅"""
    blog_ids = [user_blog.blog_id for user_blog in g.user.user_blogs]
    blogs_count = Blog.query.filter(Blog.id.in_(blog_ids)).count()
    blogs = Blog.query.filter(Blog.id.in_(blog_ids)).limit(10)
    posts = Post.query.filter(Post.blog_id.in_(blog_ids)).filter(~Post.hide).order_by(
        Post.published_at.desc()).paginate(page, 15)
    g.user.last_read_at = datetime.datetime.now()
    db.session.add(g.user)
    db.session.commit()
    return render_template('account/subscription.html', blogs=blogs, blogs_count=blogs_count,
                           posts=posts)


@bp.route('/subscribed_blogs', defaults={'page': 1})
@bp.route('/subscribed_blogs/page/<int:page>')
@UserPermission()
def subscribed_blogs(page):
    blog_ids = [user_blog.blog_id for user_blog in g.user.user_blogs]
    blogs = Blog.query.filter(Blog.id.in_(blog_ids)).paginate(page, 24)
    return render_template('account/subscribed_blogs.html', blogs=blogs)


@bp.route('/collection', defaults={'page': 1})
@bp.route('/collection/page/<int:page>')
@UserPermission()
def collection(page):
    posts = None
    return render_template('account/collection.html', posts=posts)

