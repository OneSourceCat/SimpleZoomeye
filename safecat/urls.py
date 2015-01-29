from django.conf.urls import patterns, include, url
from hostcrawler.views import *
from hostcrawler.models import *
from django.contrib import admin
from safecat import settings
admin.autodiscover()

urlpatterns = patterns('',
    ('^index/$',index),
    ('^login/$',account_login),
    ('^logout/$',logout),
    ('^active/$',active),
    ('^search/$',search),
    ('^register/$',account_register),
    ('^test/$',test),
    ('^attack/$',attack_module),
    url(r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)
