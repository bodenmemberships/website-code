from django.conf.urls import url

from . import views

# app_name='spe_blog'
urlpatterns = [
    # ex: /articles/articles/index
    url(r'^articles/index/$', views.article_index, name='article_index'),
    # ex: /articles/briefs/index
    url(r'^briefs/index/$', views.brief_index, name='brief_index'),
    # ex: /articles/publications/(?P<publication_code>)/issues
    url(r'^publications/(?P<publication_code>[0-9A-Za-z-_./]+)/issues/$', views.issue, name='issue'),
    # ex: /articles/article/?
    url(r'^article/(?P<article_id>[0-9]+)/$', views.article_detail, name='article_detail'),
    # ex: /articles/brief/?
    url(r'^brief/(?P<brief_id>[0-9]+)/$', views.brief_detail, name='brief_detail'),
]
