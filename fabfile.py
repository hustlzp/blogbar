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
            run('git reset --hard HEAD')
            run('git pull')
            with prefix('source venv/bin/activate'):
                run('pip install -r requirements.txt')
                run('python manage.py db upgrade')
            run('supervisorctl restart blogbar')


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
    run('supervisorctl restart celery')
    run('supervisorctl restart celerybeat')
    run('supervisorctl restart celeryflower')


def remote_grab():
    """启动feed抓取"""
    env.host_string = config.HOST_STRING
    with cd('/var/www/blogbar'):
        with prefix('source venv/bin/activate'):
            run('python manage.py remote_grab')