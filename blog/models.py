from django.db import models
from django.urls import reverse
from users.models import UserProfile
import markdown
# strip_tags 去掉 HTML 文本的全部 HTML 标签
from django.utils.html import strip_tags
# Create your models here.

class Tag(models.Model):
    name=models.CharField(max_length=64,verbose_name='标签名')
    class Meta:
        verbose_name='标签云'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.name
class Category(models.Model):
    name=models.CharField(max_length=64,verbose_name='分类名')
    class Meta:
        verbose_name='分类'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.name

class ArticlesBlog(models.Model):
    title=models.CharField(max_length=32,verbose_name='标题')
    summary=models.CharField(max_length=64,verbose_name='摘要',default='')
    content=models.TextField(verbose_name='文章内容')
    create_time=models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    modify_time=models.DateTimeField(verbose_name='修改时间',auto_now=True)
    is_delete=models.BooleanField(verbose_name='文章是否删除')
    is_publish=models.BooleanField(verbose_name='文章是否发布')
    author=models.ForeignKey(UserProfile,verbose_name='作者',on_delete=models.CASCADE,)
    tag=models.ManyToManyField(Tag,verbose_name='标签',blank=True)
    category=models.ForeignKey(Category,verbose_name='分类',on_delete=models.CASCADE,)
    comments=models.IntegerField(verbose_name='评论数',default=0)
    favours=models.IntegerField(verbose_name='点赞数',default=0)
    class Meta:
        verbose_name='博客文章'
        verbose_name_plural=verbose_name
        ordering=['-create_time']

    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'article_id':self.id})

    def save(self, *args, **kwargs):
        # 如果没有填写摘要
        if not self.summary:
            # 首先实例化一个 Markdown 类，用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.content))[:64]

        # 调用父类的 save 方法将数据保存到数据库中
        super(ArticlesBlog, self).save(*args, **kwargs)
    def __str__(self):
        return self.title

class FavourTable(models.Model):
    favour_user=models.ForeignKey(UserProfile,verbose_name='点赞用户',on_delete=models.CASCADE,)
    favour_article=models.ForeignKey(ArticlesBlog,verbose_name='点赞文章',on_delete=models.CASCADE,)
    is_favour=models.BooleanField(verbose_name='是否点赞')
    class Meta:
        verbose_name='点赞记录表'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.favour_user