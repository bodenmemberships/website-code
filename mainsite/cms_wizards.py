# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site

from cms.models import Page
from cms.utils import permissions

from cms.wizards.wizard_pool import wizard_pool
from cms.wizards.wizard_base import Wizard

from .forms import CreateCMSPageForm, CreateCMSSubPageForm

from .forms import ArticleCreationForm
from spe_blog.models import Article

class ArticleCreationWizard(Wizard):
    pass

article_wizard = ArticleCreationWizard(
    title="New Article",
    weight=95,
    form=ArticleCreationForm,
    description="Create an article",
)

class CMSPageWizard(Wizard):

    def user_has_add_permission(self, user, page=None, **kwargs):
        if not page or not page.site_id:
            site = Site.objects.get_current()
        else:
            site = Site.objects.get(pk=page.site_id)
        return permissions.has_page_add_permission(
            user, page, position="right", site=site)


class CMSSubPageWizard(Wizard):

    def user_has_add_permission(self, user, page=None, **kwargs):
        if not page or page.application_urls:
            # We can't really add a sub-page to a non-existant page. Or to an
            # app-hooked page.
            return False
        if not page.site_id:
            site = Site.objects.get_current()
        else:
            site = Site.objects.get(pk=page.site_id)
        return permissions.has_page_add_permission(
            user, page, position="last-child", site=site)


cms_page_wizard = CMSPageWizard(
    title=_(u"New SPE page"),
    weight=90,
    form=CreateCMSPageForm,
    model=Page,
    description=_(u"Create a new page next to the current page.")
)

cms_subpage_wizard = CMSSubPageWizard(
    title=_(u"New SPE sub page"),
    weight=91,
    form=CreateCMSSubPageForm,
    model=Page,
    description=_(u"Create a page below the current page.")
)

wizard_pool.register(article_wizard)
wizard_pool.register(cms_page_wizard)
wizard_pool.register(cms_subpage_wizard)

