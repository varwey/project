from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'yqzbw.views.home', name='home'),
    # url(r'^yqzbw/', include('yqzbw.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','search.views.lasting_search'),
    url(r'^hudie/$','search.views.hudie'),
    url(r'^tail/(\w+)/$','search.views.tail'),
    url(r'^total/$','search.views.total'),
    url(r'^jindu/$','search.views.jindu'),
    url(r'^check/$','search.views.check'),
    url(r'^save_record/$','search.views.save_record')
)
