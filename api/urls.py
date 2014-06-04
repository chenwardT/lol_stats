from django.conf.urls import url, patterns, include

from rest_framework import routers

from api.views import (SummonerViewSet,
                       ChampionViewSet,
                       ItemViewSet,
                       SummonerSpellViewSet,
                       PlayerViewSet,
                       RawStatViewSet,
                       GameViewSet,)

router = routers.DefaultRouter()
router.register(r'summoners', SummonerViewSet)
router.register(r'champions', ChampionViewSet)
router.register(r'items', ItemViewSet)
router.register(r'spells', SummonerSpellViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'stats', RawStatViewSet)
router.register(r'games', GameViewSet)

urlpatterns = patterns('api',
                       url(r'^', include(router.urls)),
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)