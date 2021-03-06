
from django.db.models import Q
from django.forms.widgets import Media as WidgetsMedia
from django.contrib.sites.models import Site
from django.contrib.admin.templatetags.admin_static import static
from django.core.urlresolvers import reverse

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import SmartSnippetPointer, SmartSnippet, Variable
from .settings import (
    shared_sites, include_orphan, restrict_user, USE_BOOTSTRAP_ACE)
from django.conf import settings
import itertools


def variables_media(media, variables=None):
    variables = variables or []
    media.add_js([static('admin/js/SmartSnippetLib.js')])
    media.add_js(
        itertools.chain(*[var.js for var in variables])
    )
    media.add_css(
        {'all': itertools.chain(*[var.css for var in variables])})


def add_variables_media(context):
    if not context:
        return
    formMedia = context.get('media')
    if not formMedia:
        return
    variables = context.get('variables')
    variables_media(formMedia, variables)


class SmartSnippetPlugin(CMSPluginBase):
    shared_sites = shared_sites
    include_orphan = include_orphan
    restrict_user = restrict_user

    change_form_template = 'smartsnippets/snippet_change_form.html'

    model = SmartSnippetPointer
    name = 'Smart Snippet'
    render_template = 'smartsnippets/plugin.html'
    text_enabled = True

    @property
    def media(self):

        if not USE_BOOTSTRAP_ACE:
            media_obj = super(SmartSnippetPlugin, self).media
        else:
            media_obj = WidgetsMedia(
                js=((
                    static('admin/js/core.js'),
                    static('admin/js/admin/RelatedObjectLookups.js'),
                    static('libs/jquery-2.1.1.min.js'),
                    static('libs/bootstrap/js/bootstrap.min.js'),
                    static('admin/js/custom.js'), )
                ),
                css={
                    'all': (
                        '//fonts.googleapis.com/css?family=Open+Sans:400,300',
                        static('libs/bootstrap/css/bootstrap.css'),
                        static('libs/ace/css/ace.min.css'),
                        static('admin/css/custom.css'), )
                    }
            )

        media_obj.add_js(
            (reverse('admin:jsi18n'),
             static('admin/js/SmartSnippetLib.js'),
             static('admin/js/jquery.init.js'),
             static('admin/js/default.jQuery.init.js')))

        if not USE_BOOTSTRAP_ACE:
            media_obj.add_css({
                'all': (
                    static('admin/css/forms.css'),
                    static('admin/css/base.css'),
                    static('css/tipTip.css'),
                    static('admin/css/snippet_plugin_default.css'), )
            })
            media_obj.add_js((
                static('js/jquery.tipTip.minified.js'),
                static('admin/js/snippet_plugin_default.js'), )
            )
        return media_obj

    def response_add(self, request, obj, **kwargs):
        response = super(SmartSnippetPlugin, self)\
            .response_add(request, obj, **kwargs)
        if hasattr(response, 'context_data'):
            response.context_data['plugin'] = obj
        return response

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        try:
            snippet = SmartSnippet.objects.get(
                id=int(request.GET.get('snippet', '')))
        except (ValueError, SmartSnippet.DoesNotExist):
            snippet = None
        else:
            empty_plugin_vars = self._make_vars_for_rendering(snippet)
            extra_context.update({'variables': empty_plugin_vars})

        response = super(SmartSnippetPlugin, self).add_view(
            request, form_url, extra_context)

        if snippet and hasattr(response, 'context_data'):
            self._change_snippet_plugin_for_preview(
                response.context_data, snippet)
            add_variables_media(response.context_data)
        return response

    def _make_vars_for_rendering(self, snippet, plugin=None):
        """
        Create plugin variables instances prepared for template rendering.
        """
        plugin = plugin or SmartSnippetPointer(snippet=snippet)
        selected_snippet_vars = snippet.variables.all()

        existing_plugin_vars = plugin.variables.filter(
            snippet_variable__in=selected_snippet_vars)
        existing_snippet_var_ids = set([
            plugin_var.snippet_variable.id
            for plugin_var in existing_plugin_vars])
        # add empty model instances; these are not saved in the db and are
        #   created just for rendering purpose
        empty_plugin_vars = [
            Variable(snippet=plugin, snippet_variable=snippet_var)
            for snippet_var in selected_snippet_vars
            if snippet_var.id not in existing_snippet_var_ids]
        return sorted(
            list(existing_plugin_vars) + empty_plugin_vars,
            key=lambda v: (v.snippet_variable._order, v.snippet_variable.name))

    def _change_snippet_plugin_for_preview(self, context, snippet):
        """
        The plugin instance rendered in the context needs to correspond to
        the new selected snippet in order for it to render its template code.
        If this is not changed for the context, the plugin that is saved
        in the db will get rendered in the preview box(which is not what
        we want if the snippet gets changed).
        """
        empty_plugin = SmartSnippetPointer(snippet=snippet)
        # copy all attributes from the cms plugin to the plugin instance
        #   in order for cms to render it as if it exists
        empty_plugin.__dict__.update(context['plugin'].__dict__)
        empty_plugin.pk = empty_plugin.id
        context['plugin'] = empty_plugin
        context['original'] = context['plugin']

    def change_view(self, request, object_id, *args, **kwargs):
        extra_context = kwargs.get('extra_context', None) or {}

        try:
            selected_snippet = SmartSnippet.objects.get(
                id=int(request.GET.get('snippet', '')))
        except (ValueError, SmartSnippet.DoesNotExist):
            selected_snippet = None

        plugin = SmartSnippetPointer.objects.get(pk=object_id)
        snippet_changed = (selected_snippet and
            selected_snippet.id != plugin.snippet.id)

        if snippet_changed:
            variables = self._make_vars_for_rendering(
                selected_snippet, plugin)
        else:
            snippet_vars = plugin.snippet.variables.all()
            variables = plugin.variables.filter(
                snippet_variable__in=snippet_vars
            ).order_by('snippet_variable___order', 'snippet_variable__name')

        extra_context.update({'variables': variables})
        kwargs['extra_context'] = extra_context
        response = super(SmartSnippetPlugin, self).change_view(
            request, object_id, *args, **kwargs)

        context = getattr(response, 'context_data', None)
        add_variables_media(context)
        if snippet_changed and context:
            adminform = response.context_data.get('adminform')
            if not adminform:
                return response
            adminform.form.initial['snippet'] = selected_snippet.id
            self._change_snippet_plugin_for_preview(
                response.context_data, selected_snippet)
        return response

    def render(self, context, instance, placeholder):
        context.update({'content': instance.render(context)})
        return context

    def save_model(self, request, obj, form, change):
        super(SmartSnippetPlugin, self).save_model(request, obj, form, change)
        vars = obj.snippet.variables.all()
        for var in vars:
            v, _ = Variable.objects.get_or_create(snippet=obj, snippet_variable=var)
            v.value = request.REQUEST.get('_'+var.name+'_', '')
            v.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "snippet":
            f = Q(sites=Site.objects.get_current())
            if self.shared_sites:
                f |= Q(sites__name__in=self.shared_sites)
            kwargs["queryset"] = SmartSnippet.objects.filter(f).distinct()
        return (super(SmartSnippetPlugin, self)
                .formfield_for_foreignkey(db_field, request, **kwargs))

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(SmartSnippetPlugin, self).formfield_for_dbfield(
            db_field, **kwargs)
        if db_field.name == "snippet":
            # hide related widget buttons
            formfield.widget.can_add_related = \
                formfield.widget.can_change_related = \
                formfield.widget.can_delete_related = False
        return formfield

    def icon_src(self, instance):
        return settings.STATIC_URL + u"images/snippet.png"

    def icon_alt(self, instance):
        if instance.snippet:
            return instance.snippet.name
        return ""

plugin_pool.register_plugin(SmartSnippetPlugin)
