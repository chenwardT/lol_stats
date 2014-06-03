from rest_framework import serializers

from api.models import Summoner, Champion, Item, SummonerSpell, Player, RawStat, Game


class RawStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawStat


class GameSerializer(serializers.ModelSerializer):
    stats = RawStatSerializer(many=False)

    class Meta:
        model = Game
        fields = ('id', 'summoner_id', 'champion_id', 'create_date', 'game_id', 'game_mode', 'game_type',
                  'invalid', 'ip_earned', 'level', 'map_id', 'spell_1', 'spell_2', 'stats', 'sub_type',
                  'team_id', 'region')


class SummonerSerializer(serializers.ModelSerializer):
    game_set = GameSerializer(many=True)

    class Meta:
        model = Summoner
        fields = ('id', 'summoner_id', 'name', 'profile_icon_id', 'revision_date', 'summoner_level', 'region',
                  'last_update', 'game_set')


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