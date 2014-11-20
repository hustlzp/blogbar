# coding: utf-8
from .github_issue import GitHubIssueSpider


class LifeSingerSpider(GitHubIssueSpider):
    url = 'https://github.com/lifesinger/lifesinger.github.com/issues?q=label:blog'
    title = '岁月如歌'
    author = '玉伯'