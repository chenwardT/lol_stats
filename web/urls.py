from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lol_stats.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^about/', 'api.views.about', name='about'),

    # TODO: these regexs are NOT robust
    # this requires a string after summoner_info/ (consider pointing to blank search page when no arg)
    url(r'^summoner_info/(?P<search_str>\w+( \w+)*$)', 'api.views.summoner_info', name='summoner_info'),

    url(r'^admin/', include(admin.site.urls)),

)
