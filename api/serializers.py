"""
Django REST Framework serializers.
"""

from rest_framework import serializers

from api.models import *


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


class LeagueForLeagueEntrySerializer(serializers.ModelSerializer):
    """
    A serializer that returns league data.

    Returned data is intended to be nested within a serialized LeagueEntry.
    """
    class Meta:
        model = League
        fields = ('region', 'queue', 'name', 'tier')


class LeagueEntrySerializer(serializers.ModelSerializer):
    """
    A serializer that returns league entry data.
    """
    league = LeagueForLeagueEntrySerializer(many=False)

    class Meta:
        model = LeagueEntry
        fields = ('division', 'is_fresh_blood', 'is_hot_streak', 'is_inactive', 'is_veteran', 'league_points',
        'player_or_team_id', 'player_or_team_name', 'wins', 'series_losses', 'series_progress', 'series_target',
        'series_wins', 'league')


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


class TeamStatDetailSerializer(serializers.ModelSerializer):
    """
    A serializer that returns team stat detail data.
    """
    class Meta:
        model = TeamStatDetail
        exclude = ('id', 'team')


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
    league_entries = LeagueEntrySerializer(source='get_league_entries')
    team_stat_detail = TeamStatDetailSerializer(source='get_team_stat_detail')

    class Meta:
        model = Team
        fields = ('create_date', 'full_id', 'last_game_date', 'modify_date', 'name', 'last_join_date',
        'second_last_join_date', 'third_last_join_date', 'status', 'tag', 'roster', 'region', 'league_entries',
        'team_stat_detail')


class AggregatedStatSerializer(serializers.ModelSerializer):
    """
    A serializer that returns AggregatedStat data.

    This is nested within PlayerStatsSummarySerializer.
    """
    class Meta:
        model = AggregatedStat
        exclude = ('id', 'player_stats')

class PlayerStatsSummarySerializer(serializers.ModelSerializer):
    """
    A serializer that returns PlayerStatsSummary data.

    This is nested within PlayerStatSerializer.
    """
    aggregated_stats = AggregatedStatSerializer(many=False, source='get_aggregated_stat')
    modify_date_str = serializers.Field(source='modify_date_str')

    class Meta:
        model = PlayerStatsSummary
        fields = ('wins', 'losses', 'modify_date_str', 'player_stat_summary_type', 'aggregated_stats')

class PlayerStatSerializer(serializers.ModelSerializer):
    """
    A serializer that returns PlayerStat data.

    Also contains related PlayerStatsSummary and AggregatedStat data.
    """
    summoner = serializers.Field(source='summoner.name')
    player_stats_summary_set = PlayerStatsSummarySerializer(many=True, source='playerstatssummary_set')

    class Meta:
        model = PlayerStat
        fields = ('summoner', 'player_stats_summary_set')