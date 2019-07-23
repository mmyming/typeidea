from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db import models

# Create your models here.
class Link(models.Model):
    STATUS_ITEMS = (
        (1, '正常'),
        (2, '删除'),
    )
    title = models.CharField(max_length=50, verbose_name='标题')
    href = models.URLField(verbose_name='链接')#默认长度200
    status = models.PositiveIntegerField(default=1, choices=STATUS_ITEMS, verbose_name='状态')
    weight = models.PositiveIntegerField(
        default=1,choices=zip(range(1,6),range(1,6)),
        verbose_name='权重',
        help_text='权重越高显示顺序越靠前'
    )

    owner = models.ForeignKey(User, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '友链'


class SideBar(models.Model):
    STATUS_ITEMS = (
        (1, '展示'),
        (2, '删除'),
    )
    SIDE_TYPE = (
        (1, 'HTML'),
        (2, '最新文章'),
        (3, '最热文章'),
        (4, '最新评论'),
    )
    title = models.CharField(max_length=50, verbose_name='标题')
    display_type = models.PositiveIntegerField(
        default=1,choices=SIDE_TYPE,verbose_name='展示类型'
    )
    status = models.PositiveIntegerField(default=1, choices=STATUS_ITEMS, verbose_name='状态')
    content = models.CharField(max_length=500,blank=True,verbose_name='内容',
                               help_text='如果设置的不是HTML类型，可为空5')

    owner = models.ForeignKey(User, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    @classmethod
    def get_all(cls):
        return cls.objects.filter(status=1)

    @property
    def content_html(self):
        '''直接渲染模版'''
        from blog.models import Post
        from comment.models import Comment
        result = ''
        if self.display_type == 1: #HTML
            result = self.content
        elif self.display_type == 2: #最新文章
            context = {
                'posts':Post.latest_posts()
            }
            result = render_to_string('config/blocks/sidebar_posts.html',context)
        elif self.display_type == 3: #最热文章
            context = {
                'posts': Post.hot_posts()
            }
            result = render_to_string('config/blocks/sidebar_posts.html', context)
        elif self.display_type == 4: # 最新评论
            context = {
                'comments':Comment.objects.filter(status=1)
            }
            result = render_to_string('config/blocks/sidebar_comments.html', context)

        return result

    class Meta:
        verbose_name = verbose_name_plural = '侧边栏'
