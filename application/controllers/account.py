# coding: utf-8
from flask import render_template, Blueprint, redirect, request, url_for
from ..forms import SigninForm, SignupForm
from ..utils.account import signin_user, signout_user
from ..utils.permissions import VisitorPermission, UserPermission
from ..models import db, User

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


@bp.route('/subscription')
@UserPermission()
def subscription():
    """我的订阅"""
    return render_template('account/subscription.html')
