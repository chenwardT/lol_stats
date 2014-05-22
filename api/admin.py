from django.contrib import admin
from api.models import *

# Register your models here.

class SummonerAdmin(admin.ModelAdmin):
    list_display = ('summoner_id', 'name', 'region')
    list_filter = ('region',)
    ordering = ('name',)

admin.site.register(Summoner, SummonerAdmin)
admin.site.register(Champion)
admin.site.register(Item)
admin.site.register(SummonerSpell)
admin.site.register(Player)
admin.site.register(RawStat)
admin.site.register(Game)