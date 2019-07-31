from django.contrib.auth.models import User
from django.db import models
import mistune

# Create your models here.
class Post(models.Model):
    STATUS_ITEMS = (
        (1,'上线'),
        (2,'草稿'),
        (3,'删除'),
    )
    title = models.CharField(max_length=50,verbose_name='标题')
    desc = models.CharField(max_length=255,blank=True,verbose_name='摘要')
    category = models.ForeignKey('Category',verbose_name='分类')
    tag  = models.ManyToManyField('Tag',blank=True,verbose_name='标签')

    content = models.TextField(verbose_name='内容',help_text='注解：目前仅支持MarkDown格式数据')
    status = models.PositiveIntegerField(default=1,choices=STATUS_ITEMS,verbose_name='状态')
    owner = models.ForeignKey(User,verbose_name='作者')
    content_html = models.TextField(verbose_name='正文html代码',blank=True,editable=False)

    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')

    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            post_list = []
        else:
            post_list = tag.post_set.filter(status=1).select_related('owner','category')

        return post_list, tag
    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            post_list = []
        else:
            post_list = category.post_set.filter(status=1).select_related('owner', 'category')

        return post_list, category

    @classmethod
    def latest_posts(cls):
        queryset = cls.objects.filter(status=1)

        return queryset

    @classmethod
    def hot_posts(cls):
        return cls.objects.filter(status=1)

    def save(self, *args,**kwargs):
        self.content_html = mistune.markdown(self.content)
        super().save(*args,**kwargs)

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']

class Category(models.Model):
    STATUS_ITEMS = (
        (1, '可用'),
        (2, '删除'),
    )
    name = models.CharField(max_length=50,verbose_name='名称')
    status = models.PositiveIntegerField(default=1,choices=STATUS_ITEMS,verbose_name='状态')
    is_nav = models.BooleanField(default=False,verbose_name='是否为导航')

    owner = models.ForeignKey(User,verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    @classmethod
    def get_navs(cls):
        categories =cls.objects.filter(status=1)
        nav_categories = []
        normal_categories = []
        for c in categories:
            if c.is_nav:
                nav_categories.append(c)
            else:
                normal_categories.append(c)
        return {
            'navs': nav_categories,
            'categories': normal_categories
        }

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '分类'


class Tag(models.Model):
    STATUS_ITEMS = (
        (1, '正常'),
        (2, '删除'),
    )
    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.PositiveIntegerField(default=1, choices=STATUS_ITEMS, verbose_name='状态')

    owner = models.ForeignKey(User, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '标签'

