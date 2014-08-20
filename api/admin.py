"""
Django admin site configuration for API module.
"""

from django.contrib import admin
from api.models import *


class SummonerAdmin(admin.ModelAdmin):
    list_display = ('summoner_id', 'name', 'region')
    list_filter = ('region',)
    ordering = ('name',)
    search_fields = ('name', 'region', 'id')


class ChampionAdmin(admin.ModelAdmin):
    list_display = ('champion_id', 'name')
    search_fields = ('name',)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'name', 'group')
    search_fields = ('name', 'description')


class SummonerSpellAdmin(admin.ModelAdmin):
    list_display = ('spell_id', 'name')
    search_fields = ('name',)


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('summoner', 'participant_of', 'region')


class RawStatAdmin(admin.ModelAdmin):
    list_display = ('game_id', 'timestamp', 'belongs_to', 'champion_played', 'win')


class GameAdmin(admin.ModelAdmin):
    list_display = ('game_id', 'create_date_str', 'summoner_id', 'champion_id', 'win', 'region')
    list_filter = ('region',)


class LeagueAdmin(admin.ModelAdmin):
    list_display = ('region', 'queue', 'name', 'tier')
    list_filter = ('region', 'queue', 'name', 'tier')


class LeagueEntryAdmin(admin.ModelAdmin):
    list_display = ('player_or_team_name', 'division', 'is_fresh_blood', 'is_hot_streak', 'is_inactive', 'is_veteran',
                    'league_points', 'player_or_team_id', 'wins', 'series_wins', 'series_losses', 'series_progress',
                    'series_target', 'league')
    list_filter = ('division', 'league')


class TeamStatDetailInline(admin.TabularInline):
    model = TeamStatDetail


class MatchHistorySummaryInline(admin.TabularInline):
    model = MatchHistorySummary


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_date_str', 'full_id', 'last_game_date_str', 'last_joined_ranked_team_queue_date_str',
                    'modify_date_str', 'last_join_date_str', 'second_last_join_date_str',
                    'third_last_join_date_str', 'status', 'tag', 'roster')
    search_fields = ('name',)
    inlines = [
        TeamStatDetailInline,
        MatchHistorySummaryInline,
    ]

class MatchHistorySummaryAdmin(admin.ModelAdmin):
    list_display = ('game_id', 'kills', 'assists', 'deaths', 'date_str', 'game_mode', 'invalid', 'map_id',
                    'opposing_team_kills', 'opposing_team_name', 'win', 'team')
    list_filter = ('team',)


class TeamMemberInfoInline(admin.TabularInline):
    model = TeamMemberInfo


class RosterAdmin(admin.ModelAdmin):
    list_display = ('owner_id', '__unicode__')
    inlines = [
        TeamMemberInfoInline,
    ]


class TeamMemberInfoAdmin(admin.ModelAdmin):
    list_display = ('get_summoner', 'invite_date_str', 'join_date_str', 'player_id', 'status', 'roster')


class TeamStatDetailAdmin(admin.ModelAdmin):
    list_display = ('team_stat_type', 'average_games_played', 'wins', 'losses', 'team')


admin.site.register(Summoner, SummonerAdmin)
admin.site.register(Champion, ChampionAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(SummonerSpell, SummonerSpellAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(RawStat, RawStatAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(League, LeagueAdmin)
admin.site.register(LeagueEntry, LeagueEntryAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(MatchHistorySummary, MatchHistorySummaryAdmin)
admin.site.register(Roster, RosterAdmin)
admin.site.register(TeamMemberInfo, TeamMemberInfoAdmin)
admin.site.register(TeamStatDetail, TeamStatDetailAdmin)