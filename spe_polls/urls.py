from django.conf.urls import patterns, url
from .views import Vote

urlpatterns = patterns('',  # NOQA
    url(r'^vote/?$', Vote.as_view(), name='vote'),
)
