#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import *

# name属性是给这个url起个别名，可以在模版中引用而不用担心urls文件中url的修改 引用方式为{% url 'czm_blog_list' %}
urlpatterns = patterns('czmblog.views',
    url(r'^czm_blog_list/$', 'czm_blog_list', name='czm_blog_list'),
    url(r'^czm_blog/(?P<blog_id>\d+)/$', 'czm_blog_show', name='czm_blog_show'),
    url(r'^czm_blog/tag/(?P<tag_id>\d+)/$', 'filter_czm_blog_by_tag', name='filter_czm_blog_by_tag'),
    url(r'^czm_blog_add/$','czm_blog_add',name='czm_blog_add'),
    url(r'^czm_blog_update/(?P<blog_id>\d+)/$', 'czm_blog_update',name='czm_blog_update'),
    url(r'^czm_blog_delete/(?P<blog_id>\d+)/$', 'czm_blog_delete', name='czm_blog_delete'),
    url(r'^czm_blog_comment/(?P<blog_id>\d+)/$', 'czm_blog_comment_add', name='czm_blog_comment_add'),
    url(r'^contact/$', 'czm_blog_contact', name='contact'),

)