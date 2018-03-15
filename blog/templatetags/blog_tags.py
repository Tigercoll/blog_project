#!/usr/bin/env python
#_*_coding:utf-8_*_
__author__ = 'Tiger'
from django import template

from ..models import ArticlesBlog,Tag,Category

register = template.Library()

@register.simple_tag
def get_recent_article(num=5):
    return ArticlesBlog.objects.filter(is_publish=True,is_delete=False)[:num]

@register.simple_tag
def get_categories():
    return  Category.objects.all()

@register.simple_tag
def get_tag():
    return Tag.objects.all()