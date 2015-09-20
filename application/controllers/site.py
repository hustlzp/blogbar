# coding: utf-8
import hashlib
from flask import render_template, Blueprint, current_app, request, abort, get_template_attribute, json
from werkzeug.contrib.atom import AtomFeed
from ..models import db, Blog, Post, ApprovementLog

bp = Blueprint('site', __name__)

LATEST_POSTS_PER = 10


@bp.route('/', defaults={'page': 1})
@bp.route('/page/<int:page>')
def index(page):
    """首页"""
    recommend_posts = Post.query.filter(Post.recommend). \
        order_by(Post.published_at.desc()).paginate(page, 15)
    posts = Post.query.filter(~Post.hide).filter(Post.blog.has(Blog.is_approved)).order_by(
        Post.published_at.desc()).limit(10)
    return render_template('site/index.html', posts=posts, recommend_posts=recommend_posts)


@bp.route('/load_posts', methods=['POST'])
def load_posts():
    """加载文章"""
    page = request.form.get('page', 1, type=int)
    posts = Post.query.filter(~Post.hide).filter(Post.blog.has(Blog.is_approved)).order_by(
        Post.published_at.desc()).paginate(page, LATEST_POSTS_PER).items
    macro = get_template_attribute('macros/post/_latest_posts.html', 'render_latest_posts')
    return json.dumps({
        'result': True,
        'html': macro(posts)
    })


@bp.route('/approve_results', defaults={'page': 1})
@bp.route('/approve_results/page/<int:page>')
def approve_results(page):
    logs = ApprovementLog.query
    unprocessed_logs = logs.filter(ApprovementLog.status == -1).order_by(
        ApprovementLog.created_at.desc())
    processed_logs = logs.filter(ApprovementLog.status != -1).order_by(
        ApprovementLog.created_at.desc()).paginate(page, 20)
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


@bp.route('/wiki')
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
