from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^publications/$', views.publications, name='publications'),
    url(r'^publication/new/$', views.publication_new, name='publication_new'),
#    url(r'^publication/(?P<pk>\d+)/edit/$', views.pub_edit, name='publication_edit'),
    url(r'^publication/submit/$', views.publication_submit, name='publication_submit'),
]