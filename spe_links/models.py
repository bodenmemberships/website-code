# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

# import datetime
from cms.models import CMSPlugin
from cms.models import Page
from cms.models.fields import PageField
from django.db import models
# from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible  # only if you need to support Python 2
class SpeLinkCategory(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    # Adding class name; if present will be used instead of the name lower case
    class_name = models.CharField(max_length=255, blank=True, null=True)
    # Adding category url if present will show all link to the url location
    show_all_page = PageField(
        verbose_name=_('Show all - Page URL'), blank=True, null=True,
        on_delete=models.SET_NULL,
        help_text=_('A page has priority over an external URL'))
    show_all_external = models.URLField(
        _('Show all - External URL'), blank=True,
        help_text=_('e.g. http://example.com/thank-you'))

    def __str__(self):  # __unicode__ on Python 2
        return self.title

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def get_absolute_url(self):
        if self.show_all_page:
            page = Page.objects.get(pk=self.show_all_page.id)
            url = page.get_absolute_url()
        else:
            url = self.show_all_external
        return url


@python_2_unicode_compatible  # only if you need to support Python 2
class SpeLink(models.Model):
    category = models.ForeignKey(SpeLinkCategory, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, null=True)
    page_url = PageField(
        verbose_name=_('Page URL'), blank=True, null=True,
        on_delete=models.SET_NULL,
        help_text=_('A page has priority over an external URL'))
    external_url = models.URLField(
        _('External URL'), blank=True,
        help_text=_('e.g. http://example.com/thank-you'))

    def __str__(self):  # __unicode__ on Python 2
        return self.title

    class Meta:
        verbose_name = "link"
        ordering = ['category__title', 'title']

    def get_absolute_url(self):
        if self.show_all_page:
            page = Page.objects.get(pk=self.page_url.id)
            url = page.get_absolute_url()
        else:
            url = self.external_url
        return url


@python_2_unicode_compatible
class SpeLinkPluginModel(CMSPlugin):
    category = models.ForeignKey(SpeLinkCategory)

    def __str__(self):
        return self.category.title
