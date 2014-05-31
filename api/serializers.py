from api.models import Summoner, Champion, Item, SummonerSpell, Player, RawStat, Game
from rest_framework import serializers


class SummonerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Summoner
        # All fields except pk
        fields = tuple([x for x in Summoner._meta.get_all_field_names() if x != u'id'])


class ChampionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Champion
        fields = tuple([x for x in Champion._meta.get_all_field_names() if x != u'id'])


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = tuple([x for x in Item._meta.get_all_field_names() if x != u'id'])


class SummonerSpellSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummonerSpell
        #fields = tuple([x for x in SummonerSpell._meta.get_all_field_names() if x != u'id'])
        fields = ('spell_id', 'summoner_level', 'name', 'key', 'description')


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = tuple([x for x in Player._meta.get_all_field_names() if x != u'id'])


class RawStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawStat
        fields = tuple([x for x in RawStat._meta.get_all_field_names() if x != u'id'])


class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = tuple([x for x in Game._meta.get_all_field_names() if x != u'id'])