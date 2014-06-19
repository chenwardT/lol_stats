from django.conf.urls import url, patterns, include

from rest_framework import routers

from api.views import (ChampionViewSet,
                       ItemViewSet,
                       SummonerSpellViewSet,
                       PlayerViewSet,
                       RawStatViewSet,
                       GameViewSet,
                       SummonerList,
                       SummonerDetail,
                       #SummonerViewSet,
)

router = routers.DefaultRouter()
#router.register(r'summoners', SummonerViewSet)
router.register(r'champions', ChampionViewSet)
router.register(r'items', ItemViewSet)
router.register(r'spells', SummonerSpellViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'stats', RawStatViewSet)
router.register(r'games', GameViewSet)

urlpatterns = patterns('api',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^task_state/', 'views.get_task_state', name='task_state'),
    url(r'^summoners/(?P<region>\w+$)', SummonerList.as_view(), name='summoner-list'),
    url(r'^summoners/(?P<region>\w+)/(?P<name>\w+( \w+)*$)', SummonerDetail.as_view(), name='summoner-detail')
)