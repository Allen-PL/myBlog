# -*- coding: utf-8 -*-


from django.contrib import admin
from django.db import models
from blog.models import Article, Friend, Comment
from mdeditor.widgets import MDEditorWidget


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'published', 'is_top', 'allow_comments', 'publish_time')
    list_filter = ('published', 'is_top', 'publish_time', 'views')
    fields = ('name', 'cover', 'content', 'excerpt', 'type', 'published', 'is_top', 'tags', 'allow_comments')
    readonly_fields = ('excerpt',)
    exclude = ('publish_time',)
    search_fields = ('name', 'slug')
    ordering = ('-create_time', 'published', 'is_top', 'publish_time')
    list_per_page = 20
    formfield_overrides = {
        models.TextField: {'widget': MDEditorWidget}
    }


class FriendAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'position', 'active')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('c_name', )


admin.site.register(Article, ArticleAdmin)
admin.site.register(Friend, FriendAdmin)
admin.site.register(Comment, CommentAdmin)