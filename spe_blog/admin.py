# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Article, Category, Publication, Issue, Editorial 
from .models import Brief, ArticleDetailPage, BriefDetailPage, TopicsPage
from mainsite.models import Tier1Discipline

class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    exclude = ['auto_tags']
    filter_horizontal = ('topics', )
    fieldsets = (
        (None, {
            'fields': (
                'publication', 'print_volume', 'print_issue', 'sponsored', 'category', 'title', 'slug', 'teaser', 'author', 'introduction', 'article_text', 'date', 'disciplines', 'topics', 'tags'
            ),
        }),
        (_('Image'), {
            'classes': ('collapse',),
            'fields': (
                'picture',
                'picture_alternate',
                'picture_attribution',
                'picture_caption',
            ),
        }),
        (_('Free'), {
            'classes': ('collapse',),
            'fields': (
                'free',
                ('free_start', 'free_stop'),
            ),
        }),
    )

class ArticleEditor(Article):
    class Meta:
        proxy = True
        verbose_name_plural = "articles (editor view)"

class ArticleEditorAdmin(ArticleAdmin):
    prepopulated_fields = {"slug": ("title",)}
    exclude = ['auto_tags']
    filter_horizontal = ('topics', )
    fieldsets = (
        (None, {
            'fields': (
                'publication', 'print_volume', 'print_issue', 'sponsored', 'category', 'title', 'slug', 'teaser', 'author', 'introduction', 'article_text', 'date', 'disciplines', 'topics', 'tags'
            ),
        }),
        (_('Image'), {
            'classes': ('collapse',),
            'fields': (
                'picture',
                'picture_alternate',
                'picture_attribution',
                'picture_caption',
            ),
        }),
        (_('Free'), {
            'classes': ('collapse',),
            'fields': (
                'free',
                ('free_start', 'free_stop'),
            ),
        }),
        (None, {
            'fields': (
                'published',
                ),
        }),
    ) 

class BriefAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    exclude = ['auto_tags']
    filter_horizontal = ('topics', )
    fieldsets = (
        (None, {
            'fields': (
                'publication', 'print_volume', 'print_issue', 'category', 'title', 'slug', 'article_text', 'date', 'topics', 'tags'
            ),
        }),
        (_('Image'), {
            'classes': ('collapse',),
            'fields': (
                'picture',
                'picture_alternate',
            ),
        }),
        (_('Free'), {
            'classes': ('collapse',),
            'fields': (
                'free',
                ('free_start', 'free_stop'),
            ),
        }),
    )

class BriefEditor(Brief):
    class Meta:
        proxy = True
        verbose_name_plural = "briefs (editor view)"

class BriefEditorAdmin(BriefAdmin):
    prepopulated_fields = {"slug": ("title",)}
    exclude = ['auto_tags']
    filter_horizontal = ('topics', )
    fieldsets = (
        (None, {
            'fields': (
                'publication', 'print_volume', 'print_issue', 'category', 'title', 'slug', 'article_text', 'date', 'topics', 'tags'
            ),
        }),
        (_('Image'), {
            'classes': ('collapse',),
            'fields': (
                'picture',
                'picture_alternate',
            ),
        }),
        (_('Free'), {
            'classes': ('collapse',),
            'fields': (
                'free',
                ('free_start', 'free_stop'),
            ),
        }),
        (None, {
            'fields': (
                'published',
                ),
        }),
    )

#    def get_form(self, request, obj=None, **kwargs):
#        if obj and obj.free:
#            self.exclude = []
#        return super(ArticleAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleEditor, ArticleEditorAdmin)
admin.site.register(Brief, BriefAdmin)
admin.site.register(BriefEditor, BriefEditorAdmin)
admin.site.register(Editorial)
admin.site.register(Category)
admin.site.register(Publication)
admin.site.register(Issue)
admin.site.register(ArticleDetailPage)
admin.site.register(BriefDetailPage)
admin.site.register(TopicsPage)
