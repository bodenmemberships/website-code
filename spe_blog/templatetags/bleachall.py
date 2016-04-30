from django import template
import bleach

register = template.Library()


@register.filter
def bleachall(value):
    """
    removes images from the text
    """
    try:
        value = bleach.clean(value, strip=True)
        return value
    except:
        pass
    return ''
