"""blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from .views import *
from .feeds import AllPostsRssFeed
app_name='blog'
urlpatterns = [
    path('',IndexView.as_view(),name='index' ),
    path('article/<int:article_id>',DetailView.as_view(), name='detail'),
    re_path(r'^categories/(?P<category_id>[0-9]+)?$',CategoryView.as_view(), name='categories'),
    path('tag/<int:tag_id>',TagView.as_view(), name='tag'),
    path('archives/',ArchiveView.as_view(), name='archives'),
    path('all/rss/', AllPostsRssFeed(), name='rss'),
    # path('search/',search,name='search')
]
