# -*- coding: utf-8 -*-

# Borrowing heavily from Aldryn's Tag Manager

# Add: {% load google_tag_manager_tags %} to top of template
# Immediately after <body> tag add: {% google_tag_manager THE_TAG_ID %}
#   or if GOOGLE_TAG_MANAGER_ID is set in settings.py: {% google_tag_manager %}

from __future__ import unicode_literals

from django.conf import settings
from django.template import Library

register = Library()


@register.inclusion_tag("google_tag_manager/google_tag_manager.html")
def google_tag_manager(tag_id=''):
    if not tag_id and hasattr(settings, 'GOOGLE_TAG_MANAGER_ID'):
        tag_id = settings.GOOGLE_TAG_MANAGER_ID
    return {
        'tag_id': tag_id
    }
