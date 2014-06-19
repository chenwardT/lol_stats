from rest_framework import serializers

from api.models import Summoner, Champion, Item, SummonerSpell, Player, RawStat, Game


class RawStatSerializer(serializers.ModelSerializer):
    """
    A serializer that returns match statistics.
    """
    class Meta:
        model = RawStat


class GameSerializer(serializers.ModelSerializer):
    """
    A serializer that returns a single match's data as well as all
    associated statistics.
    """
    stats = RawStatSerializer(many=False)

    class Meta:
        model = Game
        fields = ('id', 'summoner_id', 'champion_id', 'create_date', 'game_id', 'game_mode', 'game_type',
                  'invalid', 'ip_earned', 'level', 'map_id', 'spell_1', 'spell_2', 'stats', 'sub_type',
                  'team_id', 'region')


class SummonerSerializer(serializers.ModelSerializer):
    """
    A serializer that returns basic summoner data as well as all related
    historical match data from their point of view.
    """
    game_set = GameSerializer(many=True)

    class Meta:
        model = Summoner
        fields = ('id', 'summoner_id', 'name', 'profile_icon_id', 'revision_date', 'summoner_level', 'region',
                  'last_update', 'game_set')


class ChampionSerializer(serializers.ModelSerializer):
    """
    A serializer that returns champion data.
    """
    class Meta:
        model = Champion


class ItemSerializer(serializers.ModelSerializer):
    """
    A serializer that returns item data.
    """
    class Meta:
        model = Item


class SummonerSpellSerializer(serializers.ModelSerializer):
    """
    A serializer that returns summoner spell data.
    """
    class Meta:
        model = SummonerSpell


class PlayerSerializer(serializers.ModelSerializer):
    """
    A serializer that returns match participant data.
    """
    class Meta:
        model = Player