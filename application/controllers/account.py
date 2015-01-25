# coding: utf-8
from flask import render_template, Blueprint, redirect, request, url_for, g
from ..forms import SigninForm, SignupForm
from ..utils.account import signin_user, signout_user
from ..utils.permissions import VisitorPermission, UserPermission
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
        signin_user(user)
        return redirect(url_for('site.index'))
    return render_template('account/signup.html', form=form)


@bp.route('/signout')
def signout():
    """登出"""
    signout_user()
    return redirect(request.referrer or url_for('site.index'))


@bp.route('/subscription', defaults={'page': 1})
@bp.route('/subscription/page/<int:page>')
@UserPermission()
def subscription(page):
    """我的订阅"""
    blog_ids = [user_blog.blog_id for user_blog in g.user.user_blogs]
    blogs = Blog.query.filter(Blog.id.in_(blog_ids))
    posts = Post.query.filter(Post.blog_id.in_(blog_ids)).filter(~Post.hide).order_by(
        Post.created_at.desc()).paginate(page, 15)
    return render_template('account/subscription.html', blogs=blogs, posts=posts)
