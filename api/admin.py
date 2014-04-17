from django.contrib import admin
from api.models import *

# Register your models here.

#class SummonerAdmin(admin.ModelAdmin):
#    pass

admin.site.register(Summoner)
admin.site.register(Champion)
admin.site.register(Item)
admin.site.register(SummonerSpell)
admin.site.register(Player)
admin.site.register(RawStat)
admin.site.register(Game)