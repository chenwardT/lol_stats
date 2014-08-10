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


class LeagueEntrySerializer(serializers.ModelSerializer):
    """
    A serializer that returns league entry data.
    """
    class Meta:
        model = LeagueEntry
        exclude = ('id',)


class LeagueSerializer(serializers.ModelSerializer):
    """
    A serializer that returns league data.
    """
    leagueentry_set = LeagueEntrySerializer(many=True)
    class Meta:
        model = League
        fields = ('region', 'queue', 'name', 'tier', 'leagueentry_set')


class MatchHistorySummarySerializer(serializers.ModelSerializer):
    """
    A serializer that returns team match history summary data.
    """
    class Meta:
        model = MatchHistorySummary
        exclude = ('id',)


class TeamMemberInfoSerializer(serializers.ModelSerializer):
    """
    A serializer that returns team member info data.

    Instead of containing a `player_id` field, it resolve the ID a Summoner object,
    which yields the summoner's name, otherwise returns `player_id`.
    Timestamps are converted into human-readable format.
    """
    summoner = serializers.Field(source='get_summoner')
    invite_date_str = serializers.Field(source='invite_date_str')
    join_date_str = serializers.Field(source='join_date_str')

    class Meta:
        model = TeamMemberInfo
        fields = ('invite_date_str', 'join_date_str', 'summoner', 'status')


class RosterSerializer(serializers.ModelSerializer):
    """
    A serializer that returns team roster data.

    Instead of containing an `owner_id` field, it resolves the ID to a Summoner object,
    which yields the summoner's name, otherwise returns `owner_id`.
    Team members of the roster are nested within.
    """
    teammemberinfo_set = TeamMemberInfoSerializer(many=True)
    owner = serializers.Field(source='get_summoner')
    class Meta:
        model = Roster
        fields = ('owner', 'teammemberinfo_set')


class TeamSerializer(serializers.ModelSerializer):
    """
    A serializer that returns team data.

    Timestamps are converted into human-readable format.
    """
    roster = RosterSerializer(many=False)

    create_date = serializers.Field(source='create_date_str')
    last_game_date = serializers.Field(source='last_game_date_str')
    last_joined_ranked_team_queue_date = serializers.Field(source='last_joined_ranked_team_queue_str')
    modify_date = serializers.Field(source='modify_date_str')
    last_join_date = serializers.Field(source='last_join_date_str')
    second_last_join_date = serializers.Field(source='second_last_join_date_str')
    third_last_join_date = serializers.Field(source='third_last_join_date_str')

    class Meta:
        model = Team
        fields = ('create_date', 'full_id', 'last_game_date', 'modify_date', 'name', 'last_join_date',
        'second_last_join_date', 'third_last_join_date', 'status', 'tag', 'roster', 'region')


class TeamStatDetailSerializer(serializers.ModelSerializer):
    """
    A serializer that returns team stat detail data.
    """
    class Meta:
        model = TeamStatDetail
        exclude = ('id',)

