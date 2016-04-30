from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import SpeLinkPluginModel, SpeLink
from django.utils.translation import ugettext as _


class SpeLinkPluginPublisher(CMSPluginBase):
    model = SpeLinkPluginModel  # model where plugin data are saved
    module = _("Links")
    name = _("Links Plugin")  # name of the plugin in the interface
    render_template = "spe_links/plugins/links_plugin.html"
    cache = False

    def render(self, context, instance, placeholder):
        if instance.category and instance.category.id:
            instance.links = SpeLink.objects.filter(category_id__exact=instance.category.id).values().order_by("title")

        context.update({'instance': instance})

        return context


plugin_pool.register_plugin(SpeLinkPluginPublisher)  # register the plugin
