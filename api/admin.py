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
    list_display = ('division', 'is_fresh_blood', 'is_hot_streak', 'is_inactive', 'is_veteran',
                    'league_points', 'player_or_team_id', 'player_or_team_name', 'wins',
                    'series_wins', 'series_losses', 'series_progress', 'series_target', 'league')
    list_filter = ('division', 'league')

admin.site.register(Summoner, SummonerAdmin)
admin.site.register(Champion, ChampionAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(SummonerSpell, SummonerSpellAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(RawStat, RawStatAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(League, LeagueAdmin)
admin.site.register(LeagueEntry, LeagueEntryAdmin)