# coding: utf-8
import hashlib
from flask import render_template, Blueprint, current_app, request, abort
from werkzeug.contrib.atom import AtomFeed
from ..models import db, Blog, Post, ApprovementLog

bp = Blueprint('site', __name__)


@bp.route('/', defaults={'page': 1})
@bp.route('/page/<int:page>')
def index(page):
    """首页"""
    recommend_posts = Post.query.filter(Post.recommend). \
        order_by(Post.published_at.desc()).paginate(page, 15)

    blogs_query = Blog.query.filter(Blog.is_approved)
    blogs_count = blogs_query.count()
    latest_blogs = blogs_query.order_by(Blog.created_at.desc()).limit(15)

    posts_query = Post.query.filter(~Post.hide). \
        filter(Post.blog.has(Blog.is_approved))
    posts_count = posts_query.count()
    latest_posts = posts_query.order_by(Post.published_at.desc()).limit(10)
    return render_template('site/index.html', latest_posts=latest_posts,
                           latest_blogs=latest_blogs, blogs_count=blogs_count,
                           posts_count=posts_count, recommend_posts=recommend_posts)


@bp.route('/approve_results', defaults={'page': 1})
@bp.route('/approve_results/page/<int:page>')
def approve_results(page):
    logs = ApprovementLog.query
    unprocessed_logs = logs.filter(ApprovementLog.status == -1).order_by(
        ApprovementLog.updated_at.desc())
    processed_logs = logs.filter(ApprovementLog.status != -1).order_by(
        ApprovementLog.status.desc(),
        ApprovementLog.updated_at.desc()).paginate(page, 20)
    return render_template('site/approve_results.html', unprocessed_logs=unprocessed_logs,
                           processed_logs=processed_logs)


@bp.route('/suggest')
def suggest():
    return render_template('site/suggest.html')


@bp.route('/about')
def about():
    """关于页"""
    return render_template('site/about.html')


@bp.route('/disclaimer')
def disclaimer():
    """免责声明"""
    return render_template('site/disclaimer.html')

@bp.route('/help')
def wiki():
    """帮助"""
    return render_template('site/wiki.html')

@bp.route('/feed/posts.xml')
def posts_feed():
    config = current_app.config
    domain = config.get('SITE_DOMAIN')
    feed = AtomFeed("Blogbar编辑推荐",
                    subtitle='当你和世界不一样，那就让你不一样。',
                    feed_url="%s%s" % (domain, request.path),
                    url=domain,
                    id=domain)
    recommend_posts = Post.query.filter(Post.recommend). \
        order_by(Post.published_at.desc()).limit(15)
    for post in recommend_posts:
        feed.add(post.title, post.content, content_type='html', author=post.blog.author,
                 url=post.url, id=post.url, updated=post.published_at)
    response = feed.get_response()
    response.headers['Content-Type'] = 'application/xml'
    return response


@bp.route('/weixin')
def weixin():
    config = current_app.config
    weixin_token = config.get('WEIXIN_TOKEN')

    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')

    temp_str = ''.join(sorted([weixin_token, timestamp, nonce]))
    hash_sha1 = hashlib.sha1(temp_str)
    temp_str = hash_sha1.hexdigest()
    if temp_str == signature:
        return echostr
    else:
        abort(500)
