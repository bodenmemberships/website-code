from django import template
import bleach

register = template.Library()


@register.filter
def bleachimages(value, arg):
    """
    removes images from the text
    """
    try:
        value = bleach.clean('<span>is not allowed</span>', strip=True)
        # arg = int(arg)
        # if arg:
        #     return value / arg
        return value
    except:
        pass
    return ''
