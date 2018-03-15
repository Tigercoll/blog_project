from django.shortcuts import render,get_object_or_404
from .models import *
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
import markdown
from django.db.models.aggregates import Count
from django.db.models import Q
# Create your views here.
class IndexView(View):
    def get(self,request):
        all_articles=ArticlesBlog.objects.filter(is_delete=False,is_publish=True)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_articles,1, request=request)
        article_list = p.page(page)
        return render(request,'index.html', {'article_list': article_list,})

class DetailView(View):
    def get(self,request,article_id):
        article_list=get_object_or_404(ArticlesBlog,id=article_id,is_delete=False,is_publish=True)
        if ArticlesBlog.objects.filter(id=int(article_id-1),is_delete=False,is_publish=True):
            article_previous=get_object_or_404(ArticlesBlog,id=int(article_id-1),is_delete=False,is_publish=True)
        else:
            article_previous=False
        if ArticlesBlog.objects.filter(id=int(article_id+1),is_delete=False,is_publish=True):
            article_next=get_object_or_404(ArticlesBlog, id=int(article_id +1),is_delete=False,is_publish=True)
        else:
            article_next=False
        article_list.content = markdown.markdown(article_list.content,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        return render(request,'detail.html',{'article': article_list,'article_previous':article_previous,'article_next':article_next})

class CategoryView(View):
    def get(self,request,category_id):
        if category_id:
            category=get_object_or_404(Category,id=category_id,)
            all_articles=ArticlesBlog.objects.filter(category=category,is_delete=False,is_publish=True)
            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1
            # Provide Paginator with the request object for complete querystring generation
            p = Paginator(all_articles,1, request=request)
            article_list = p.page(page)
            return render(request,'index.html', {'article_list': article_list,'category':category})
        else:
            category_list = Category.objects.filter(articlesblog__is_delete=False,articlesblog__is_publish=True).annotate(num=Count('articlesblog'))
        return render(request, 'category.html', {'category_list': category_list})



class TagView(View):
    def get(self, request, tag_id):
        tag = get_object_or_404(Tag, id=tag_id)
        all_articles = ArticlesBlog.objects.filter(tag=tag,is_delete=False,is_publish=True)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_articles, 1, request=request)
        article_list = p.page(page)
        return render(request, 'index.html', {'article_list': article_list, 'tag': tag})

class ArchiveView(View):
    def get(self,request):
        all_articles = ArticlesBlog.objects.filter(is_delete=False, is_publish=True)
        return render(request, 'archives.html', {'article_list': all_articles, })

def search(request):
    q=request.GET.get('q','')
    error_msg=''
    print(q)
    if q:
        all_articles = ArticlesBlog.objects.filter(Q(title__icontains=q) | Q(content__icontains=q)).filter(is_delete=False,is_publish=True)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_articles, 1, request=request)
        article_list = p.page(page)
        return render(request, 'index.html', {'error_msg': error_msg,
                                              'article_list': article_list,'q':q})
    else:
        error_msg='请输入关键词'
        return render(request, 'index.html', {'error_msg': error_msg,})