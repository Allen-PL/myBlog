# -*- coding: utf-8 -*-

import datetime
import markdown
from django.db import models
from uuslug import slugify
from blog.storage import PathAndRename
from django.urls import reverse
from mdeditor.fields import MDTextField
from taggit.managers import TaggableManager

BlogTypes = (
    ('l', '星辰大海'),
    ('j', '碎碎念'),
    ('w', '旅行'),
)


class Article(models.Model):
    """文章详情"""
    name = models.CharField(u'标题', max_length=150, unique=True)
    slug = models.SlugField(u'链接', default='#', null=True, blank=True)
    cover = models.ImageField(upload_to=PathAndRename("cover"), verbose_name=u'封面')
    type = models.CharField(max_length=1, choices=BlogTypes, default='l', verbose_name=u'类型')
    content = MDTextField(u'内容', )
    excerpt = models.TextField(u'摘要', )
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'修改时间')
    published = models.BooleanField(u'发布', default=True)
    is_top = models.BooleanField(u'置顶', default=False)
    allow_comments = models.BooleanField('开启评论', default=True)
    publish_time = models.DateTimeField(u'发布时间', null=True)
    views = models.PositiveIntegerField(u'浏览量', default=0)
    tags = TaggableManager(blank=True, help_text='标签用英文逗号隔开')

    class Meta:
        ordering = ['-is_top', '-update_time']
        verbose_name = u'文章'
        verbose_name_plural = u'文章'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        modified = kwargs.pop("modified", True)
        if modified:
            self.update_time = datetime.datetime.utcnow()

        if self.published and not self.publish_time:
            self.publish_time = datetime.datetime.utcnow()

        # 生成摘要
        # 获取readmore位置
        readmore_index = self.content.find('<!--more-->')

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.toc',
            'markdown.extensions.headerid',
        ])
        # 截取readmore前的字符串作为摘要并用markdown渲染
        self.excerpt = md.convert(self.content[:readmore_index])

        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    """评论表"""
    c_name = models.CharField(verbose_name="评论用户名",max_length=16,null=False)
    c_photo = models.CharField(verbose_name="评论这头像",max_length=256)
    c_content = models.TextField(verbose_name="评论内容",max_length=512)
    zan = models.IntegerField(verbose_name="点赞数",default=0)
    create_time = models.DateTimeField(verbose_name="评论时间",auto_now_add=True)
    article_id = models.ForeignKey(verbose_name="关联文章",to=Article,on_delete=None)
    p_id = models.IntegerField(verbose_name="顶级评论",default=0)
    comment_id = models.OneToOneField(verbose_name="自关联",to='self',on_delete=None,default=0)

    class Meta:
        verbose_name = "评论表"
        verbose_name_plural = "评论表"

    def __str__(self):
        return self.c_name


class Friend(models.Model):
    """
    友情链接
    """
    name = models.CharField(u'名称', max_length=100, default='')
    link = models.URLField(u'链接', default='')
    cover = models.ImageField(upload_to=PathAndRename("link"), blank=True, verbose_name=u'头像')
    desc = models.TextField(u'描述', default='未添加描述')
    position = models.SmallIntegerField(u'位置', default=1)
    active = models.BooleanField(u'激活', default=True)

    class Meta:
        ordering = ['position']
        verbose_name = u'友情链接'
        verbose_name_plural = u'友情链接'

    def __str__(self):
        return self.name

