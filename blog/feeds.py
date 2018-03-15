#!/usr/bin/env python
#_*_coding:utf-8_*_
__author__ = 'Tiger'
from django.contrib.syndication.views import Feed

from .models import ArticlesBlog


class AllPostsRssFeed(Feed):
    # 显示在聚合阅读器上的标题
    title = "Tigercoll的博客"

    # 通过聚合阅读器跳转到网站的地址
    link = "/"

    # 显示在聚合阅读器上的描述信息
    description = "Tigercoll的博客文章"

    # 需要显示的内容条目
    def items(self):
        return ArticlesBlog.objects.filter(is_publish=True,is_delete=False)

    # 聚合器中显示的内容条目的标题
    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    # 聚合器中显示的内容条目的描述
    def item_description(self, item):
        return item.content