"""
Django REST Framework serializers.
"""

from rest_framework import serializers

from api.models import (Summoner,
                        Champion,
                        Item,
                        SummonerSpell,
                        Player,
                        RawStat,
                        Game,
                        League,
                        LeagueEntry,
                        Team,
                        MatchHistorySummary,
                        Roster,
                        TeamMemberInfo,
                        TeamStatDetail)


class SparseSummonerSerializer(serializers.ModelSerializer):
    """
    A serializer that returns sparse summoner data.

    Used by PlayerSerializer.
    """
    class Meta:
        model = Summoner
        fields = ('summoner_id', 'name')


class ChampionSerializer(serializers.ModelSerializer):
    """
    A serializer that returns champion data.
    """
    class Meta:
        model = Champion
        fields = ('champion_id', 'name', 'key')


class PlayerSerializer(serializers.ModelSerializer):
    """
    A serializer that returns match participant data.
    """
    champion = ChampionSerializer()
    summoner = SparseSummonerSerializer()

    class Meta:
        model = Player
        fields = ('summoner', 'champion', 'team_id')


class RawStatSerializer(serializers.ModelSerializer):
    """
    A serializer that returns match statistics.
    """
    class Meta:
        model = RawStat
        exclude = ('id',)


class GameSerializer(serializers.ModelSerializer):
    """
    A serializer that returns a single match's data as well as all
    associated statistics.
    """
    stats = RawStatSerializer(many=False)
    player_set = PlayerSerializer(many=True)

    class Meta:
        model = Game
        fields = ('summoner_id', 'champion_id', 'create_date', 'game_id', 'game_mode', 'game_type',
                  'invalid', 'ip_earned', 'level', 'map_id', 'spell_1', 'spell_2', 'stats', 'sub_type',
                  'team_id', 'region', 'player_set', 'last_update', 'champion_key')


class SummonerSerializer(serializers.ModelSerializer):
    """
    A serializer that returns basic summoner data as well as all related
    historical match data from their point of view.
    """
    #game_set = GameSerializer(many=True)

    class Meta:
        model = Summoner
        fields = ('id', 'summoner_id', 'name', 'profile_icon_id', 'revision_date', 'summoner_level', 'region',
                  'last_update')


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


class LeagueSerializer(serializers.ModelSerializer):
    """
    A serializer that returns league data.
    """
    class Meta:
        model = League
        exclude = ('id',)


class LeagueEntrySerializer(serializers.ModelSerializer):
    """
    A serializer that returns league entry data.
    """
    class Meta:
        model = LeagueEntry
        exclude = ('id',)


class TeamSerializer(serializers.ModelSerializer):
    """
    A serializer that returns team data.
    """
    class Meta:
        model = Team
        exclude = ('id',)


class MatchHistorySummarySerializer(serializers.ModelSerializer):
    """
    A serializer that returns team match history summary data.
    """
    class Meta:
        model = MatchHistorySummary
        exclude = ('id',)


class RosterSerializer(serializers.ModelSerializer):
    """
    A serializer that returns team roster data.
    """
    class Meta:
        model = Roster
        exclude = ('id',)


class TeamMemberInfoSerializer(serializers.ModelSerializer):
    """
    A serializer that returns team member info data.
    """
    class Meta:
        model = TeamMemberInfo
        exclude = ('id',)


class TeamStatDetailSerializer(serializers.ModelSerializer):
    """
    A serializer that returns team stat detail data.
    """
    class Meta:
        model = TeamStatDetail
        exclude = ('id',)

