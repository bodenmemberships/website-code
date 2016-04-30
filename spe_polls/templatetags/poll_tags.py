from django import template
from math import ceil

#from .forms import x

register = template.Library()


@register.filter()
def in_compare_to(value, total):
    return str(int(ceil(float(value) / float(total) * 100)))

#@register.inclusion_tag('cms/plugins/poll_form.html')
#def poll_form():
#    return {'form': x(), 'action': '/some/url'}
