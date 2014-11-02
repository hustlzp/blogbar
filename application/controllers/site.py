# coding: utf-8
from flask import render_template, Blueprint
from ..models import Blog

bp = Blueprint('site', __name__)


@bp.route('/')
def index():
    """首页"""
    blogs = Blog.query
    return render_template('site/index.html', blogs=blogs)


@bp.route('/about')
def about():
    """关于页"""
    return render_template('site/about.html')