# coding: utf-8
import requests
from flask import current_app, render_template, url_for
from .helper import absolute_url_for


def send_active_mail(user):
    """发送激活链接到用户邮箱"""
    active_url = absolute_url_for('account.active', token=user.token)
    return send_mail(user.email,
                     '发送激活链接',
                     '激活 Blogbar 账号',
                     render_template('mail/active.html', active_url=active_url))


def send_mail(to, fromname, subject, html):
    """通用的邮件发送函数，返回成功与否"""
    config = current_app.config

    url = "http://sendcloud.sohu.com/webapi/mail.send.json"
    params = {
        "api_user": config['SC_API_USER'],
        "api_key": config['SC_API_KEY'],
        "to": to,
        "from": config['SC_FROM'],
        "fromname": fromname,
        "subject": subject,
        "html": html
    }

    try:
        r = requests.post(url, data=params)
    except Exception, e:
        # TODO: 记录错误
        print(e)
        return False
    else:
        if r.status_code == 200:
            return True
        else:
            # TODO：记录错误
            print(r.text)
            return False
