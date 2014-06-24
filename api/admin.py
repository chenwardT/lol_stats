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
    list_display = ('summoner', 'participant_of')


admin.site.register(Summoner, SummonerAdmin)
admin.site.register(Champion, ChampionAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(SummonerSpell, SummonerSpellAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(RawStat)
admin.site.register(Game)