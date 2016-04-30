# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import *  # NOQA
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = i18n_patterns('',
    url(r'^admin/', include(admin.site.urls)),  # NOQA
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': {'cmspages': CMSSitemap}}),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^articles/', include('spe_blog.urls')),
    url(r'^spe_links/', include('spe_links.urls')),
    #url(r'^contact/', include('spe_contact.urls')),
    url(r'^localhost/login/do', 'mainsite.views.do_login', name='dologin'),
    url(r'^localhost/login/show', 'mainsite.views.login_show', name='showlogin'),
    url(r'^localhost/logout/', 'mainsite.views.logout', name='logout'),
    url(r'^localhost/login/', 'mainsite.views.login', name='login'),
    url(r'^polls/', include('spe_polls.urls', namespace='polls')),
    url(r'^forms/', include('djangocms_forms.urls')),
    #url(r'^filer/', include('filer.urls')),
    url(r'^', include('cms.urls')),
)

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',  # NOQA
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        ) + staticfiles_urlpatterns() + urlpatterns  # NOQA
