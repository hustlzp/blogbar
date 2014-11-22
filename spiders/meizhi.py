# coding: utf-8
import datetime
from .base import BaseSpider, get_inner_html, remove_element


class MeiZhiSpider(BaseSpider):
    url = "http://meizhi.im"
    title = "妹纸"
    author = "http://aisk.me"
    for_special_purpose = True

    @staticmethod
    def get_posts(tree):
        posts = []
        boxes = tree.cssselect('.box')
        for box in boxes:
            link = box.cssselect('a')[0]
            url = link.get('href')
            data_text = box.cssselect('.meta a')[0].text_content()
            title = "%s的妹纸" % data_text
            published_at = datetime.datetime.strptime(data_text, "%Y年%m月%d日")
            posts.append({
                'title': title,
                'url': url,
                'published_at': published_at
            })
        return posts

    @staticmethod
    def get_post(tree):
        remove_element(tree.cssselect('.box')[0])
        box_btns = tree.cssselect('.box-btns')
        map(remove_element, box_btns)
        return get_inner_html(tree.cssselect('.row')[0])
