from django.conf.urls import url, patterns

urlpatterns = patterns('summoner',
    # These regex are not robust.
    # This requires a string after summoner_info/ (consider pointing to blank search page when no arg)
    url(r'^info/(?P<summoner_name>\w+( \w+)*$)', 'views.summoner_info', name='summoner_info'),
    url(r'^async_summoner_info/', 'views.async_summoner_info', name='async_summoner_info'),
    url(r'^ajax_summoner_info/', 'views.ajax_summoner_info', name='ajax_summoner_info'),
    url(r'^recent/(?P<summoner_name>\w+( \w+)*$)', 'views.recent_games', name='recent_games'),
    url(r'^do_task$', 'views.ajax_query_start', name='do_task'),
    url(r'^ajax_query_start$', 'views.ajax_query_start', name='ajax_query_start'),
    url(r'^sum_info$', 'views.summoner_info', name='base_summoner_info'),
)