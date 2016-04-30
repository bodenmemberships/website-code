# from itertools import chain
# import requests
# import json
import re
import urlparse

from django.shortcuts import get_object_or_404
from django.http import Http404
from django.utils import timezone

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
# from cms.models.pluginmodel import CMSPlugin

from django.utils.translation import ugettext_lazy as _
from django.db import connection
from django.db.models import Q

# from django.contrib.gis.geoip import GeoIP

from .models import (
    Article, ArticlesPlugin, ArticlesListingPlugin, ArticleDetailPlugin,
    Brief, BriefPlugin, BriefListingPlugin, BriefDetailPlugin,
    Issue, IssuesByPublicationPlugin,
    Editorial, EditorialPlugin,
    BreadCrumbPlugin,
    # Publication,
    IssuesByYearPlugin,
    MarketoFormPlugin,
    TopicsListPlugin, TopicsPlugin
)
from .forms import ArticleSelectionForm, BriefSelectionForm, EditorialSelectionForm, \
    TopicsListSelectionForm, OldTopicsListSelectionForm


class ArticlePluginBase(CMSPluginBase):
    """
    Abstract base class to be used for all Article plugins.
    """

    class Meta:
        abstract = True

    allow_children = False
    cache = False
    module = _('Article')
    render_template = 'spe_blog/plugins/image_left.html'
    text_enabled = False


class ShowArticleDetailPlugin(ArticlePluginBase):
    model = ArticleDetailPlugin
    name = _("Show Article Detail")

    def render(self, context, instance, placeholder):
        now = timezone.now()
        art = get_object_or_404(Article, pk=instance.article.id)
        if instance.allow_url_to_override_selection:
            q = re.findall('(art)=(\d+)', urlparse.urlparse(context.get('request').get_full_path()).query)
            if q and q[0][0] == 'art':
                pk = int(q[0][1])
                if pk:
                    try:
                        art = get_object_or_404(Article, pk=pk)
                    except:
                        raise Http404("Article not found")
        topic_related = None
        filter_topics = art.topics.all()
        if filter_topics and instance.show_related_articles:
            filter_main = Article.objects.filter(published=True).filter(topics__in=filter_topics.all())
            filter_ex = filter_main.exclude(id=art.id)
            topic_related = filter_ex.order_by('-date')[:3]

        context.update({'article': art})
        context.update({'dateNow': now})
        context.update({'topic_articles': topic_related})
        self.render_template = 'spe_blog/plugins/article_detail.html'
        return context


class ShowArticlesPlugin(ArticlePluginBase):
    model = ArticlesPlugin
    name = _("Selected Articles ")
    form = ArticleSelectionForm

    def render(self, context, instance, placeholder):
        #        if instance.keep_original_order:
        #            queryset = Article.objects.none()
        #            for art in instance.articles.all():
        #                queryadd = Article.objects.filter(id=art.id).all()
        #                queryset = list(chain(queryset, queryadd))
        #        else:
        #            queryset = Article.objects.filter(id__in=instance.articles.all()).order_by(instance.order_by)
        queryset = Article.objects.filter(published=True).filter(id__in=instance.articles.all()).order_by(
            instance.order_by)
        context.update({'articles': queryset})
        context.update({'backcol': instance.backcol})
        if instance.all_url:
            context.update({'show_all_url': instance.all_url.get_absolute_url()})
            context.update({'show_all_text': instance.all_text})
        self.render_template = instance.template
        return context


class BriefPluginBase(CMSPluginBase):
    """
    Abstract base class to be used for all Brief plugins.
    """

    class Meta:
        abstract = True

    allow_children = False
    cache = False
    module = _('Article')
    render_template = 'spe_blog/plugins/brief_interest.html'
    text_enabled = False


class ShowBriefDetailPlugin(BriefPluginBase):
    model = BriefDetailPlugin
    name = _("Show Brief Detail")

    def render(self, context, instance, placeholder):
        now = timezone.now()
        art = get_object_or_404(Brief, pk=instance.brief.id)
        if instance.allow_url_to_override_selection:
            q = re.findall('(art)=(\d+)', urlparse.urlparse(context.get('request').get_full_path()).query)
            if q and q[0][0] == 'art':
                pk = int(q[0][1])
                if pk:
                    try:
                        art = get_object_or_404(Brief, pk=pk)
                    except:
                        raise Http404("Article not found")
        context.update({'article': art})
        context.update({'dateNow': now})
        self.render_template = 'spe_blog/plugins/brief_detail.html'
        return context


class ShowBriefPlugin(BriefPluginBase):
    model = BriefPlugin
    name = _("Selected Briefs ")
    form = BriefSelectionForm

    def render(self, context, instance, placeholder):
        queryset = Brief.objects.filter(published=True).filter(id__in=instance.briefs.all()).order_by(instance.order_by)
        context.update({'articles': queryset})
        if instance.all_url:
            context.update({'show_all_url': instance.all_url.get_absolute_url()})
            context.update({'show_all_text': instance.all_text})
        self.render_template = instance.template
        return context


class ShowBriefListingPlugin(BriefPluginBase):
    model = BriefListingPlugin
    name = _("Brief Listing")

    def render(self, context, instance, placeholder):
        # request = context.get('request')
        if instance.publication:
            qs = Brief.objects.filter(published=True).filter(publication=instance.publication)
        else:
            qs = Brief.objects.all().filter(published=True)

        if instance.category:
            qs = qs.filter(category=instance.category)

        if instance.print_volume:
            qs = qs.filter(print_volume=instance.print_volume)
        if instance.print_issue:
            qs = qs.filter(print_issue=instance.print_issue)

        qs = qs.order_by(instance.order_by)[instance.starting_with - 1:instance.cnt]
        # NOTE: add other querysets if the publication and discipline is set; need 1 for each combination
        context.update({'articles': qs})
        if instance.all_url:
            context.update({'show_all_url': instance.all_url.get_absolute_url()})
            context.update({'show_all_text': instance.all_text})
        self.render_template = instance.template
        return context


class TopicsPluginBase(CMSPluginBase):
    """
    Abstract base class to be used for all Topics plugins.
    """

    class Meta:
        abstract = True

    allow_children = False
    cache = False
    module = _('Article')
    render_template = 'spe_blog/plugins/topics_list.html'
    text_enabled = False


class ShowTopicsListPlugin(TopicsPluginBase):
    model = TopicsListPlugin
    name = _("[GOOD USE ME] Topics Listing")
    form = TopicsListSelectionForm

    def render(self, context, instance, placeholder):
        cursor = connection.cursor()
        cursor.execute('''
          select distinct(t.topics_id) as id from spe_blog_topicslistplugin_topics t
          right outer join spe_blog_topicslistplugin p on t.topicslistplugin_id = p.cmsplugin_ptr_id
          right outer join spe_blog_article_topics at on t.topics_id = at.topics_id
          right outer join spe_blog_article a on at.article_id = a.id
          where t.topicslistplugin_id = %s
          and p.cmsplugin_ptr_id is not null
          and at.topics_id is not null
          and a.publication_id = p.publication_id;
        ''', [instance.pk])
        used_topic_ids = cursor.fetchall()

        if used_topic_ids:
            in_filter = Q()
            for tid in used_topic_ids:
                in_filter = in_filter | Q(pk__in=tid)
            topics = instance.topics.filter(in_filter)
        else:
            topics = None

        context.update({'topics': topics})
        context.update({'publication': instance.publication})
        self.render_template = instance.template
        return context


class ShowTopicsListOneColPlugin(TopicsPluginBase):
    model = TopicsListPlugin
    name = _("[BAD CHANGE ME] Topics Listing 1 Column")
    form = OldTopicsListSelectionForm

    def render(self, context, instance, placeholder):
        topics = instance.topics.all()
        context.update({'topics': topics})
        context.update({'publication': instance.publication})
        self.render_template = 'spe_blog/plugins/topics_list_1col.html'
        return context


class ShowTopicsListTwoColPlugin(TopicsPluginBase):
    model = TopicsListPlugin
    name = _("[BAD CHANGE ME] Topics Listing 2 Columns")
    form = OldTopicsListSelectionForm

    def render(self, context, instance, placeholder):
        topics = instance.topics.all()
        context.update({'topics': topics})
        context.update({'publication': instance.publication})
        self.render_template = 'spe_blog/plugins/topics_list.html'
        return context


class ShowTopicsListThreeColPlugin(TopicsPluginBase):
    model = TopicsListPlugin
    name = _("[BAD CHANGE ME] Topics Listing 3 Columns")
    form = OldTopicsListSelectionForm

    def render(self, context, instance, placeholder):
        cursor = connection.cursor()
        cursor.execute('''
          select distinct(t.topics_id) as id from spe_blog_topicslistplugin_topics t
          right outer join spe_blog_topicslistplugin p on t.topicslistplugin_id = p.cmsplugin_ptr_id
          right outer join spe_blog_article_topics at on t.topics_id = at.topics_id
          right outer join spe_blog_article a on at.article_id = a.id
          where t.topicslistplugin_id = %s
          and p.cmsplugin_ptr_id is not null
          and at.topics_id is not null
          and a.publication_id = p.publication_id;
        ''', [instance.pk])
        used_topic_ids = cursor.fetchall()

        in_filter = Q()
        for tid in used_topic_ids:
            in_filter = in_filter | Q(pk__in=tid)
        topics = instance.topics.filter(in_filter)
        context.update({'topics': topics})
        context.update({'publication': instance.publication})
        self.render_template = 'spe_blog/plugins/topics_list_3col.html'
        return context


class ShowTopicsListingPlugin(TopicsPluginBase):
    model = TopicsPlugin
    name = _("Show Articles by Topics")

    def render(self, context, instance, placeholder):
        # request = context.get('request')
        art = ''
        now = timezone.now()
        if instance.allow_url_to_override_selection:
            q = re.findall('(topic)=(\d+)', urlparse.urlparse(context.get('request').get_full_path()).query)
            if q and q[0][0] == 'topic':
                pk = int(q[0][1])
                if pk:
                    art = Article.objects.all().filter(published=True).filter(publication=instance.publication).filter(
                        topics__pk=pk).order_by(instance.order_by)[instance.starting_with - 1:instance.cnt]
                else:
                    raise Http404("Topic not found")
        else:
            art = Article.objects.all().filter(published=True).filter(publication=instance.publication).filter(
                topics__pk__in=instance.topics.all()).order_by(instance.order_by).distinct()[
                  instance.starting_with - 1:instance.cnt]
        context.update({'articles': art})
        context.update({'dateNow': now})
        self.render_template = instance.template
        return context


class ShowEditorialPlugin(ArticlePluginBase):
    model = EditorialPlugin
    name = _("Editorial")
    form = EditorialSelectionForm

    def render(self, context, instance, placeholder):
        queryset = Editorial.objects.filter(id__in=instance.editorial.all())
        context.update({'editorials': queryset})
        context.update({'link': instance.lnk})
        context.update({'backcol': instance.backcol})
        self.render_template = instance.template
        return context


class ShowArticlesListingPlugin(ArticlePluginBase):
    model = ArticlesListingPlugin
    name = _("Articles Listing")

    def render(self, context, instance, placeholder):
        request = context.get('request')
        # NOTE: change this to be set in the context globally and stored server side
        ducode = None
        dcode = None
        if instance.personalized:
            ducode = request.COOKIES.get('dc')
        if instance.discipline:
            dcode = instance.discipline.code
        context.update({'ducode': ducode, 'dcode': dcode})
        # NOTE: todo - create an in clause filter with each code if there are any
        if instance.publication:
            qs = Article.objects.filter(published=True).filter(publication=instance.publication)
        else:
            qs = Article.objects.all().filter(published=True)

        if instance.categories.all():
            qs = qs.filter(category__in=instance.categories.all())

        if instance.print_volume:
            qs = qs.filter(print_volume=instance.print_volume)
        if instance.print_issue:
            qs = qs.filter(print_issue=instance.print_issue)

        if ducode:
            qs = qs.filter(disciplines=ducode).order_by(instance.order_by)[
                 instance.starting_with - 1:instance.starting_with + instance.cnt - 1]
        elif dcode:
            qs = qs.filter(disciplines=dcode).order_by(instance.order_by)[
                 instance.starting_with - 1:instance.starting_with + instance.cnt - 1]
        else:
            qs = qs.order_by(instance.order_by)[instance.starting_with - 1:instance.cnt]
        # NOTE: add other querysets if the publication and discipline is set; need 1 for each combination
        context.update({'articles': qs})
        context.update({'backcol': instance.backcol})
        if instance.all_url:
            context.update({'show_all_url': instance.all_url.get_absolute_url()})
            context.update({'show_all_text': instance.all_text})
        self.render_template = instance.template
        return context


# class ShowArticlesByUserDisciplinePlugin(ArticlePluginBase):
#     model = ArticleDisciplineByUserPluginModel
#     name = _("Show Articles by User Discipline")
#
#     def render(self, context, instance, placeholder):
#         dc = context.get('request').COOKIES.get("dc")
#         queryset = Article.objects.filter(disciplines=dc).order_by(instance.orderby)[
#                    instance.starting_with:instance.articles]
#         context.update({'articles': queryset})
#         context.update({'title': instance.title})
#         return context
#
#
# class ShowArticlesByDisciplinePlugin(ArticlePluginBase):
#     model = ArticleDisciplinePluginModel
#     name = _("Show Articles by Discipline")
#
#     def render(self, context, instance, placeholder):
#         queryset = Article.objects.filter(disciplines=instance.discipline.code).order_by(instance.orderby)[
#                    instance.starting_with:instance.articles]
#         context.update({'articles': queryset})
#         context.update({'title': instance.title})
#         return context
#
#
# class ShowArticlesFromPublicationPlugin(ArticlePluginBase):
#     model = ArticleByPublicationPluginModel
#     name = _("Show Articles From Publication")
#
#     def render(self, context, instance, placeholder):
#         queryset = Article.objects.filter(publication=instance.publication).order_by(instance.orderby)[
#                    instance.starting_with:instance.articles]
#         context.update({'articles': queryset})
#         context.update({'title': instance.title})
#         return context
#
#
# class ShowFeatureArticlesPlugin(ArticlePluginBase):
#     model = SelectedFeatureArticlePluginModel
#     name = _("Show Article From Publication")
#
#     def render(self, context, instance, placeholder):
#         queryset = Article.objects.filter(publication=instance.publication).filter(print_issue=instance.issue).filter(
#             slug=instance.slug)
#         if queryset:
#             context.update({'articles': queryset})
#         self.render_template = instance.template
#         return context


class ShowIssuesByPublicationPlugin(CMSPluginBase):
    model = IssuesByPublicationPlugin
    allow_children = False
    cache = False
    module = _('Publications')
    name = _('Issues by Publication Listing')
    text_enabled = False
    render_template = 'spe_blog/plugins/issue_channel.html'

    # render_plugin = False

    def render(self, context, instance, placeholder):
        queryset = Issue.objects.filter(publication=instance.publication).order_by('-date')[
                   instance.starting_with - 1:instance.starting_with + instance.cnt - 1]
        context.update({'publication': instance.publication})
        context.update({'issues': queryset})
        if instance.all_url:
            context.update({'show_all_url': instance.all_url.get_absolute_url()})
            context.update({'show_all_text': instance.all_text})
        context.update({'show_subscribe_url': instance.publication.subscription_url})
        self.render_template = instance.template
        return context


class ShowBreadCrumbPlugin(CMSPluginBase):
    model = BreadCrumbPlugin
    allow_children = False
    cache = False
    module = _('Publications')
    name = _('Bread Crumb')
    text_enabled = False
    render_template = 'spe_blog/plugins/bread_crumb.html'

    def render(self, context, instance, placeholder):
        context.update({'title': instance.title})
        return context


class ShowIssuesByYearPlugin(CMSPluginBase):
    model = IssuesByYearPlugin
    allow_children = False
    cache = False
    module = _('Publications')
    name = _('Issues by Year')
    text_enabled = False
    render_template = 'spe_blog/plugins/issues_by_year.html'

    def render(self, context, instance, placeholder):
        issues = Issue.objects.filter(publication=instance.publication).order_by('-date')
        context.update({'issues': issues})
        return context


class ShowMarketoFormPlugin(CMSPluginBase):
    model = MarketoFormPlugin
    allow_children = False
    cache = False
    module = _('Publications')
    name = _('Marketo Form')
    text_enabled = False
    render_template = 'spe_blog/plugins/marketo_form.html'

    def render(self, context, instance, placeholder):
        context.update({'instructions': instance.instructions})
        context.update({'marketo_form': instance.marketo_form})
        context.update({'thank_you': instance.thank_you})
        return context


plugin_pool.register_plugin(ShowArticleDetailPlugin)
plugin_pool.register_plugin(ShowArticlesPlugin)
plugin_pool.register_plugin(ShowArticlesListingPlugin)
plugin_pool.register_plugin(ShowBriefDetailPlugin)
plugin_pool.register_plugin(ShowBriefPlugin)
plugin_pool.register_plugin(ShowBriefListingPlugin)
plugin_pool.register_plugin(ShowEditorialPlugin)
plugin_pool.register_plugin(ShowIssuesByPublicationPlugin)
# plugin_pool.register_plugin(ShowBreadCrumbPlugin)
plugin_pool.register_plugin(ShowIssuesByYearPlugin)
plugin_pool.register_plugin(ShowMarketoFormPlugin)
plugin_pool.register_plugin(ShowTopicsListOneColPlugin)
plugin_pool.register_plugin(ShowTopicsListPlugin)
plugin_pool.register_plugin(ShowTopicsListTwoColPlugin)
plugin_pool.register_plugin(ShowTopicsListThreeColPlugin)
plugin_pool.register_plugin(ShowTopicsListingPlugin)
