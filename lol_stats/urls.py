from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers

from api.views import ChampionViewSet, ItemViewSet, SummonerSpellViewSet, PlayerViewSet, RawStatViewSet,\
    GameViewSet, SummonerList, SummonerDetail

admin.autodiscover()

router = routers.DefaultRouter()
#router.register(r'summoners', SummonerViewSet)
router.register(r'champions', ChampionViewSet)
router.register(r'items', ItemViewSet)
router.register(r'spells', SummonerSpellViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'stats', RawStatViewSet)
router.register(r'games', GameViewSet)

urlpatterns = patterns('',
    # All api.* routes are purely for testing, in production, views should come from a different app.
    # TODO: these regexs are NOT robust

    # This requires a string after summoner_info/ (consider pointing to blank search page when no arg)
    url(r'^summoner_info/(?P<summoner_name>\w+( \w+)*$)', 'api.views.summoner_info', name='summoner_info'),
    url(r'^async_summoner_info/', 'api.views.async_summoner_info', name='async_summoner_info'),
    url(r'^ajax_summoner_info/', 'api.views.ajax_summoner_info', name='ajax_summoner_info'),
    url(r'^recent/(?P<summoner_name>\w+( \w+)*$)', 'api.views.recent_games', name='recent_games'),
    url(r'^items/', 'api.views.view_items', name='view_items'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^summoners/(?P<region>.+)/$', SummonerList.as_view()),
    url(r'^summoners/(?P<region>.+)/(?P<summoner_id>.+$)', SummonerDetail.as_view()),
)
