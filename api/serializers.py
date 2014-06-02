from api.models import Summoner, Champion, Item, SummonerSpell, Player, RawStat, Game
from rest_framework import serializers


class SummonerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Summoner
        # All fields except pk
        #exclude = ('id',)


class ChampionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Champion
        #exclude = ('id',)


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        #exclude = ('id',)


class SummonerSpellSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummonerSpell
        #exclude = ('id',)


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        #exclude = ('id',)


class RawStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawStat
        #exclude = ('id',)


# Since Game relates to Summoner, and that requires multiple lookup fields (region + summoner ID)
# it may be wise to abandon trying to get hyperlinking and everything else to work with multiple lookup_fields
# and instead just get the API to the point where it can be used by jQuery effectively, instead of being
# completely RESTful in every sense of the word.
class GameSerializer(serializers.ModelSerializer):

    #summoner_id = serializers.RelatedField()

    class Meta:
        model = Game
        #exclude = ('id',)