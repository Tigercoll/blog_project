#!/usr/bin/env python
#_*_coding:utf-8_*_
__author__ = 'Tiger'

from haystack import indexes
from .models import ArticlesBlog


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return ArticlesBlog

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_publish=True,is_delete=False)