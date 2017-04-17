Blogbar
=======

http://www.blogbar.cc

个人博客之死，就是个人博客之生。

将信息的快速传递交给新兴媒介，让个人博客回归原来的位置：一种信息的雕刻与沉淀的工具。

世界太嘈杂，这里只有**个人**<sup>兆赫</sup>。

Blogbar，聚合个人博客。

## 技术栈

* Powered by [Flask](http://flask.pocoo.org/).
* Based on [Flask-Boost](https://github.com/hustlzp/Flask-Boost).
* Use cron to grab data periodically.
* Use [feerparser](http://pythonhosted.org/feedparser/) to parse RSS and Atom.
* Use [requests](http://docs.python-requests.org/en/latest/) and [lxml](http://lxml.de/) to grab structured data from HTML page.

## 开发环境搭建

```
git clone https://github.com/blogbar/blogbar.git
cd blogbar
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
bower install
```

将`db/blogbar.sql`导入本地数据库。

将`config/development_sample.py`另存为`config/development.py`，并按需更新配置项。

```
python manage.py run
```

## 扩展

如果一个博客不提供 Feed，但是这个博客的价值又非常高（比如 [Livid](http://livid.v2ex.com/)、[王垠](http://www.yinwang.org/)、[Lifesinger](https://github.com/lifesinger/lifesinger.github.com/issues?q=label%3Ablog)等等），可继承爬取博客的爬虫基类 BaseSpider（位于 [spiders/base.py](https://github.com/blogbar/blogbar/blob/master/spiders/base.py)）实现，步骤如下：

#### 类变量赋值

在子类中对如下类变量重新赋值：

```py
url = ""  # 网址
posts_url = ""  # 包含博文列表的网址（选填，只有当博客网址与博文列表网址不同时才需填写）
title = ""  # 博客标题
subtitle = ""  # 博客副标题（选填）
author = ""  # 博主
```

#### 重载方法

重载如下 2 个方法：

* get_posts：获取博文列表
* get_post：获取单篇博文内容

具体使用方法见 BaseSpider 类，以及用于爬取网页内容的 [lxml](http://lxml.de/) 库。

#### 调试

编写过程中如需调试抓取结果，可使用 [test_spider.py](https://github.com/blogbar/blogbar/blob/master/test_spider.py) 提供的测试方法：

* $ python test_spider.py get_posts
* $ python test_spider.py get_post
* $ python test_spider.py all

具体见 [test_spider.py](https://github.com/blogbar/blogbar/blob/master/test_spider.py)。

#### 提交

测试通过后，可发起 pull request。

#### 示例

以下是爬取 Livid 博客的示例代码：

```py
# coding: utf-8
from .base import BaseSpider, get_inner_html
from datetime import datetime


class LividSpider(BaseSpider):
    url = "http://livid.v2ex.com"
    title = "Livid"
    author = "Livid"

    @staticmethod
    def get_posts(tree):
        posts = []
        for li in tree.cssselect('.posts li'):
            date_element = li.cssselect('span')[0]
            published_at = datetime.strptime(date_element.text_content(), "%d %b %Y")
            link = li.cssselect('a')[0]
            posts.append({
                'url': link.get('href'),
                'title': link.text_content(),
                'published_at': published_at
            })
        return posts

    @staticmethod
    def get_post(tree):
        content_element = tree.cssselect('div.span10')[0]
        return get_inner_html(content_element)
```
