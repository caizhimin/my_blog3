from django.conf.urls import patterns, include, url
from django.contrib import admin
import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'my_blog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^czmblog/', include('czmblog.urls')),
    url(r'^index/$', 'czmblog.views.index', name='index')
)

urlpatterns += patterns('',
                        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                        {'document_root': BASE_DIR + '/static'}),

                        )





