# coding: utf-8
from .github_issue import GitHubIssueSpider


class FouberSpider(GitHubIssueSpider):
    url = 'https://github.com/fouber/blog'
    posts_url = 'https://github.com/fouber/blog/issues'
    title = '张云龙的个人博客'
    author = '张云龙'