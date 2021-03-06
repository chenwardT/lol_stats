"""
URL map for API module.
"""

from django.conf.urls import url, patterns, include

from api.views import (
    SummonerList,
    SummonerDetail,
    ChampionList,
    ChampionDetail,
    ItemList,
    ItemDetail,
    SummonerSpellList,
    SummonerSpellDetail,
    PlayerList,
    PlayerDetail,
    RawStatList,
    RawStatDetail,
    GameList,
    GameDetail,
    LeagueList,
    LeagueDetail,
    LeagueEntryList,
    LeagueEntryDetail,
    TeamList,
    TeamDetail,
    RosterList,
    RosterDetail,
    TeamMemberInfoList,
    TeamMemberInfoDetail,
    PlayerStatList,
    PlayerStatDetail,
    api_root)

# TODO: Consider allowing lookup by ID (check for number instead of \w+)
# TODO: Consider separating out summoner-list and summoner-region-list classes (same name in browseable API)
# TODO: Add action prefixes to endpoints such as `by-id`, `by-name`, etc.
urlpatterns = patterns('api',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^task_state$', 'views.get_task_state', name='task_state'),

    # Note: trailing slashes
    url(r'^$', api_root),

    url(r'^summoners$', SummonerList.as_view(), name='summoner-list'),
    url(r'^summoners/(?P<region>\w+)$', SummonerList.as_view(), name='summoners-region-list'),
    url(r'^summoners/(?P<region>\w+)/(?P<name>\w+( *\w+)*)$', SummonerDetail.as_view(), name='summoners-detail'),

    url(r'^champions$', ChampionList.as_view(), name='champion-list'),
    url(r'^champions/(?P<name>\w+)$', ChampionDetail.as_view(), name='champion-detail'),

    url(r'^items$', ItemList.as_view(), name='item-list'),
    url(r'^items/(?P<name>\w+( *\w+)*)$$', ItemDetail.as_view(), name='item-detail'),

    url(r'^spells$', SummonerSpellList.as_view(), name='spell-list'),
    url(r'^spells/(?P<name>\w+( *\w+)*)$$', SummonerSpellDetail.as_view(), name='spell-detail'),

    url(r'^players$', PlayerList.as_view(), name='player-list'),
    url(r'^players/(?P<name>\w+( *\w+)*)$', PlayerDetail.as_view(), name='player-detail'),

    url(r'^stats$', RawStatList.as_view(), name='stat-list'),
    url(r'^stats/(?P<game_id>\d+$)', RawStatDetail.as_view(), name='stat-detail'),

    url(r'^games$', GameList.as_view(), name='game-list'),
    url(r'^games/(?P<region>\w+)/(?P<game_id>\d+$)', GameDetail.as_view(), name='game-detail'),
    # \w matches digits, so it is important that this comes after the detail view, which uses game_id for lookup!
    url(r'^games/(?P<region>\w+)/(?P<name>\w+( *\w+)*)$', GameList.as_view(), name='game-region-name-list'),

    url(r'^leagues$', LeagueList.as_view(), name='league-list'),
    url(r'^leagues/(?P<region>\w+)$', LeagueList.as_view(), name='league-region-list'),
    url(r"^leagues/(?P<region>\w+)/(?P<queue>\w+)$", LeagueList.as_view(), name='league-region-queue-list'),
    url(r"^leagues/(?P<region>\w+)/(?P<queue>\w+)/(?P<tier>\w+)$", LeagueList.as_view(), name='league-region-queue-tier-list'),
    url(r"^leagues/(?P<region>\w+)/(?P<queue>\w+)/(?P<tier>\w+)/(?P<name>\w+('* *\w+)*)$", LeagueDetail.as_view(), name='league-detail'),

    url(r'^league-entries$', LeagueEntryList.as_view(), name='league-entry-list'),
    url(r'^league-entries/(?P<region>\w+)$', LeagueEntryList.as_view(), name='league-entry-region-list'),
    # Retrieve by player_or_team_id.
    url(r'^league-entries/(?P<region>\w+)/(?P<id>(-*\w+)*)$', LeagueEntryDetail.as_view(), name='league-entry-detail'),

    url(r'^teams$', TeamList.as_view(), name='team-list'),
    url(r'^teams/(?P<region>\w+)$', TeamList.as_view(), name='team-region-list'),
    # List by std_name.
    url(r'^teams/(?P<region>\w+)/by-member/(?P<member_name>\w+( *\w+)*)$', TeamList.as_view(), name='team-by-member-name-list'),
    # Retrieve by full_id.
    url(r'^teams/(?P<region>\w+)/by-team-id/(?P<full_id>TEAM(-*\w+)*)$', TeamDetail.as_view(), name='team-detail'),

    url(r'^rosters$', RosterList.as_view(), name='roster-list'),

    url(r'^teammemberinfo$', TeamMemberInfoList.as_view(), name='teammemberinfo-list'),

    url(r'^playerstats$', PlayerStatList.as_view(), name='playerstat-list'),
    url(r'^playerstats/(?P<region>\w+)/(?P<name>\w+( *\w+)*)$', PlayerStatDetail.as_view(), name='playerstat-detail'),

)