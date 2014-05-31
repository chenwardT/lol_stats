from api.models import Summoner, Champion, Item, SummonerSpell, Player, RawStat, Game
from rest_framework import serializers


class SummonerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Summoner


class ChampionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Champion


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item


class SummonerSpellSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummonerSpell


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player


class RawStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawStat


class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game