from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^about/', 'api.views.about', name='about'),

    # all api.* routes are purely for testing, in production only web.* routes will probably exist
    # TODO: these regexs are NOT robust
    # this requires a string after summoner_info/ (consider pointing to blank search page when no arg)
    url(r'^summoner_info/(?P<search_str>\w+( \w+)*$)', 'api.views.summoner_info', name='summoner_info'),
    url(r'^ajax_summoner_info/(?P<summoner_id>\w+$)', 'api.views.ajax_summoner_info', name='ajax_summoner_info'),
    url(r'^recent/(?P<summoner_name>\w+( \w+)*$)', 'api.views.recent_games', name='recent_games'),
    url(r'^admin/', include(admin.site.urls)),

)
