# coding: utf-8
from fabric.api import run, env, cd, prefix, shell_env
from config import load_config

config = load_config()
host_string = config.HOST_STRING


def deploy():
    """部署"""
    env.host_string = config.HOST_STRING
    with cd('/var/www/blogbar'):
        with shell_env(MODE='PRODUCTION'):
            run('supervisorctl stop blogbar')
            run('git reset --hard HEAD')
            run('git pull')
            with prefix('source venv/bin/activate'):
                run('pip install -r requirements.txt')
                run('python manage.py db upgrade')
            run('supervisorctl start blogbar')


def pull():
    """更新代码"""
    env.host_string = config.HOST_STRING
    with cd('/var/www/blogbar'):
        with shell_env(MODE='PRODUCTION'):
            run('git reset --hard HEAD')
            run('git pull')


def restart():
    """重启"""
    env.host_string = config.HOST_STRING
    run('supervisorctl restart blogbar')


def restart_celery():
    """重启celery相关进程"""
    env.host_string = config.HOST_STRING
    # 在Celery启动时，似乎需要更多内存，启动后才降下来
    # 所以这里首先关闭了其他2个进程
    run('supervisorctl stop celerybeat')
    # run('supervisorctl stop celeryflower')
    run('supervisorctl restart celery')
    run('supervisorctl start celerybeat')
    # run('supervisorctl start celeryflower')


def remote_grab():
    """启动feed抓取"""
    env.host_string = config.HOST_STRING
    with cd('/var/www/blogbar'):
        with prefix('source venv/bin/activate'):
            run('python manage.py remote_grab')
