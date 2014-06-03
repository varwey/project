from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import blog.views
from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webot.views.home', name='home'),
    # url(r'^webot/', include('webot.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^userlogin/$','blog.views.userlogin'),
    url(r'^accounts/login/$','django.contrib.auth.views.login',{'template_name':'userlogin.html'}),
    url(r'^userlogout/$','blog.views.userlogout'),
    url(r'^$','blog.views.index'),
    url(r'^configsearch/$','blog.views.configsearch'),
    url(r'^config_secretary/$','scrapy.views.config_secretary'),
    url(r'^config_topic/$','scrapy.views.config_topic'),
    url(r'^configsearch/configadd/$','blog.views.configadd'),
    url(r'^configalter/(\d+)/$','blog.views.configalter'), 
    url(r'^configtail/(\d+)/$','blog.views.configtail'), 
    url(r'^configdel/(\d+)/(\w+)/$','blog.views.configdel'), 
    url(r'^problemconfig/$','blog.views.problemconfig'),
    url(r'^listquery/$','blog.views.listquery'),
    url(r'^urlquery/$','blog.views.urlquery'),
    url(r'^collectorstate/$','blog.views.collectorstate'),
    url(r'^income_count/$','scrapy.views.income_count'),
    url(r'^income_today/$','scrapy.views.income_today'),
    url(r'^income_tables/$','scrapy.views.income_tables'),
    url(r'^income_ranking/$','scrapy.views.income_ranking'),
    url(r'^storagecount/$','blog.views.storagecount'),
    url(r'^storage_monitor/$','scrapy.views.storage_monitor'),
    url(r'^scan_count/$','blog.views.scan_count'),
    url(r'^scan_progress/$','blog.views.scan_progress'),
    url(r'^spider_server/$','blog.views.spider_server'),
    url(r'^spider_server_manger/(\d+)/(\d+)/$','blog.views.spider_server_manger'),
    url(r'^task_list/$','blog.views.task_list'),
    url(r'^task_list/(\d+)/$','blog.views.task_list_tail'),
    url(r'^task_list_manger/(\d+)/(\d+)/$','blog.views.task_list_manger'),
    url(r'^config_error/$','blog.views.config_error'),
    url(r'^task_distribution/$','blog.views.task_distribution'),
    url(r'^task_situation/$','blog.views.task_situation'),
    url(r'^time_diff/$','scrapy.views.time_diff'),
    url(r'^http_status/$','blog.views.http_status'),
    url(r'^task_tail/(\w+.\w+.\w*)/$','blog.views.task_tail'),
    url(r'^st_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT },name='media'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT },name='static'),
)
urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)


