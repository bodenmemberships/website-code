from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from cms.toolbar_pool import toolbar_pool
from cms.toolbar.items import Break
from cms.cms_toolbars import ADMIN_MENU_IDENTIFIER, ADMINISTRATION_BREAK
from cms.toolbar_base import CMSToolbar

@toolbar_pool.register
class PollToolbar(CMSToolbar):

    def populate(self):
        admin_menu = self.toolbar.get_or_create_menu(ADMIN_MENU_IDENTIFIER, _('Site'))
        position = admin_menu.find_first(Break, identifier=ADMINISTRATION_BREAK)
        menu = admin_menu.get_or_create_menu('Article Menu', _('Articles & Briefs'), position=position)
        url = reverse('admin:spe_blog_article_add')
        menu.add_sideframe_item(_('Add Article'), url=url)
        url = reverse('admin:spe_blog_article_changelist')
        menu.add_modal_item(_('List & Edit Articles'), url=url)
        url = reverse('admin:spe_blog_brief_add')
        menu.add_sideframe_item(_('Add Brief'), url=url)
        url = reverse('admin:spe_blog_brief_changelist')
        menu.add_modal_item(_('List & Edit Briefs'), url=url)
        url = reverse('admin:spe_blog_brief_add')
