"""
Django models for lol_stats project.
"""

import time

import inflection
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

# TODO: Set PKs to extant fields, if possible.


class Summoner(models.Model):
    """Maps to Riot API summoner DTO.

    Also contains timestamp for when object was last updated.
    """
    summoner_id = models.BigIntegerField()
    # Names "should" be 16 chars, but sometimes we get weird names (ex. "IS141dca1d0484dcf8adc09")
    name = models.CharField(max_length=24)
    std_name = models.CharField(max_length=24)  # This is `name` as lowercase with spaces stripped.
    profile_icon_id = models.IntegerField()
    revision_date = models.BigIntegerField()
    summoner_level = models.IntegerField()  # 'long' in DTO, but we know it's <= 30
    region = models.CharField(max_length=4)
    last_update = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        """These fields, taken together, ensure no duplicates are created."""
        unique_together = ('summoner_id', 'region')


class Champion(models.Model):
    """Maps to Riot API champion DTO."""
    champion_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    key = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name


class Item(models.Model):
    """Maps to Riot API item DTO."""
    item_id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=1024)
    name = models.CharField(max_length=64)
    plain_text = models.CharField(max_length=256, blank=True, null=True)
    group = models.CharField(max_length=64, blank=True, null=True)

    def __unicode__(self):
        return self.name


class SummonerSpell(models.Model):
    """Maps to Riot API summonerSpell DTO."""
    spell_id = models.IntegerField(primary_key=True)
    summoner_level = models.IntegerField()
    name = models.CharField(max_length=16)
    key = models.CharField(max_length=32)
    description = models.CharField(max_length=256)

    def __unicode__(self):
        return '%s' % self.name

## placeholder
#class Mastery(models.Model):
#    pass
#
## placeholder
#class Rune(models.Model):
#    pass
#
## placeholder
#class Realm(models.Model):
#    pass


#########
# GAMES #
#########


class Player(models.Model):
    """
    Maps to Riot API fellowPlayer DTO.

    fellowPlayer is related to match history query.
    """
    champion = models.ForeignKey(Champion)
    summoner = models.ForeignKey(Summoner)
    team_id = models.IntegerField()  # 100, 200
    participant_of = models.ForeignKey('Game')

    class Meta:
        ordering = ('team_id',)

    def __unicode__(self):
        return '%s on %s (Team %d)' % (self.summoner, self.champion, self.team_id)

    def region(self):
        return self.participant_of.region


class RawStat(models.Model):
    """
    Maps to Riot API RawStats DTO.

    RawStats is related to match history query.
    """
    assists = models.IntegerField(blank=True, null=True)
    barracks_killed = models.IntegerField(blank=True, null=True)
    champions_killed = models.IntegerField(blank=True, null=True)
    combat_player_score = models.IntegerField(blank=True, null=True)
    consumables_purchased = models.IntegerField(blank=True, null=True)
    damage_dealt_player = models.IntegerField(blank=True, null=True)
    double_kills = models.IntegerField(blank=True, null=True)
    first_blood = models.IntegerField(blank=True, null=True)
    gold = models.IntegerField(blank=True, null=True)
    gold_earned = models.IntegerField(blank=True, null=True)
    gold_spent = models.IntegerField(blank=True, null=True)
    item0 = models.IntegerField(blank=True, null=True)
    item1 = models.IntegerField(blank=True, null=True)
    item2 = models.IntegerField(blank=True, null=True)
    item3 = models.IntegerField(blank=True, null=True)
    item4 = models.IntegerField(blank=True, null=True)
    item5 = models.IntegerField(blank=True, null=True)
    item6 = models.IntegerField(blank=True, null=True)
    items_purchased = models.IntegerField(blank=True, null=True)
    killing_sprees = models.IntegerField(blank=True, null=True)
    largest_critical_strike = models.IntegerField(blank=True, null=True)
    largest_killing_spree = models.IntegerField(blank=True, null=True)
    largest_multi_kill = models.IntegerField(blank=True, null=True)
    legendary_items_created = models.IntegerField(blank=True, null=True)  # Number of tier 3 items built.
    level = models.IntegerField(blank=True, null=True)
    magic_damage_dealt_player = models.IntegerField(blank=True, null=True)
    magic_damage_dealt_to_champions = models.IntegerField(blank=True, null=True)
    magic_damage_taken = models.IntegerField(blank=True, null=True)
    minions_denied = models.IntegerField(blank=True, null=True)
    minions_killed = models.IntegerField(blank=True, null=True)
    neutral_minions_killed = models.IntegerField(blank=True, null=True)
    neutral_minions_killed_enemy_jungle = models.IntegerField(blank=True, null=True)
    neutral_minions_killed_your_jungle = models.IntegerField(blank=True, null=True)
    nexus_killed = models.NullBooleanField(blank=True, null=True)  # Flag specifying if the summoner got the killing blow on the nexus.
    node_capture = models.IntegerField(blank=True, null=True)
    node_capture_assist = models.IntegerField(blank=True, null=True)
    node_neutralize = models.IntegerField(blank=True, null=True)
    node_neutralize_assist = models.IntegerField(blank=True, null=True)
    num_deaths = models.IntegerField(blank=True, null=True)
    num_items_bought = models.IntegerField(blank=True, null=True)
    objective_player_score = models.IntegerField(blank=True, null=True)
    penta_kills = models.IntegerField(blank=True, null=True)
    physical_damage_dealt_player = models.IntegerField(blank=True, null=True)
    physical_damage_dealt_to_champions = models.IntegerField(blank=True, null=True)
    physical_damage_taken = models.IntegerField(blank=True, null=True)
    quadra_kills = models.IntegerField(blank=True, null=True)
    sight_wards_bought = models.IntegerField(blank=True, null=True)
    spell_1_cast = models.IntegerField(blank=True, null=True)  # Number of times first champion spell was cast.
    spell_2_cast = models.IntegerField(blank=True, null=True)  # Number of times second champion spell was cast.
    spell_3_cast = models.IntegerField(blank=True, null=True)  # Number of times third champion spell was cast.
    spell_4_cast = models.IntegerField(blank=True, null=True)  # Number of times fourth champion spell was cast.
    summon_spell_1_cast = models.IntegerField(blank=True, null=True)
    summon_spell_2_cast = models.IntegerField(blank=True, null=True)
    super_monster_killed = models.IntegerField(blank=True, null=True)
    team = models.IntegerField(blank=True, null=True)  # redundant due to Game.team_id
    team_objective = models.IntegerField(blank=True, null=True)
    time_played = models.IntegerField(blank=True, null=True)
    total_damage_dealt = models.IntegerField(blank=True, null=True)
    total_damage_dealt_to_champions = models.IntegerField(blank=True, null=True)
    total_damage_taken = models.IntegerField(blank=True, null=True)
    total_heal = models.IntegerField(blank=True, null=True)
    total_player_score = models.IntegerField(blank=True, null=True)
    total_score_rank = models.IntegerField(blank=True, null=True)
    total_time_crowd_control_dealt = models.IntegerField(blank=True, null=True)
    total_units_healed = models.IntegerField(blank=True, null=True)
    triple_kills = models.IntegerField(blank=True, null=True)
    true_damage_dealt_player = models.IntegerField(blank=True, null=True)
    true_damage_dealt_to_champions = models.IntegerField(blank=True, null=True)
    true_damage_taken = models.IntegerField(blank=True, null=True)
    turrets_killed = models.IntegerField(blank=True, null=True)
    unreal_kills = models.IntegerField(blank=True, null=True)
    victory_point_total = models.IntegerField(blank=True, null=True)
    vision_wards_bought = models.IntegerField(blank=True, null=True)
    ward_killed = models.IntegerField(blank=True, null=True)
    ward_placed = models.IntegerField(blank=True, null=True)
    win = models.NullBooleanField(blank=True, null=True)  # Flag specifying whether or not this game was won.

    def __unicode__(self):
        return 'Stats for %s' % Game.objects.get(stats=self)

    def __iter__(self):
        """Generator that returns field names and values for each value that is not None."""
        for i in self._meta.get_all_field_names():
            if getattr(self, i) is not None:
                yield '{}: {}'.format(inflection.humanize(i), getattr(self, i))

    def belongs_to(self):
        return Game.objects.get(stats=self).summoner_id

    def champion_played(self):
        return Game.objects.get(stats=self).champion_id

    def game_id(self):
        return Game.objects.get(stats=self).game_id

    def region(self):
        return Game.objects.get(stats=self).region

    def timestamp(self):
        return Game.objects.get(stats=self).create_date_str()


class Game(models.Model):
    """
    Maps to Riot API Game DTO.

    Instead of summonerId and championId, foreign keys to those objects are used.
    RawStat object is related to by these objects via 1-to-1.
    Player objects point to this to allow reverse-querying of match participants.

    To get a match history (QuerySet), given a region (R) and Summoner name (N):

    Game.objects.filter(summoner_id=Summoner.objects.filter(region=R).filter(name=N)

    Alternatively, given a Summoner object (S):

    S.game_set.all()
    """
    summoner_id = models.ForeignKey(Summoner)
    champion_id = models.ForeignKey(Champion)
    create_date = models.BigIntegerField()
    game_id = models.BigIntegerField()
    game_mode = models.CharField(max_length=16)
    game_type = models.CharField(max_length=16)
    invalid = models.BooleanField()
    ip_earned = models.IntegerField()
    level = models.IntegerField()
    map_id = models.IntegerField()
    spell_1 = models.ForeignKey(SummonerSpell, related_name='spell_1')
    spell_2 = models.ForeignKey(SummonerSpell, related_name='spell_2')
    stats = models.OneToOneField(RawStat)
    sub_type = models.CharField(max_length=24)
    team_id = models.IntegerField()
    region = models.CharField(max_length=4)
    last_update = models.DateTimeField(auto_now=True)

    champion_key = models.CharField(max_length=32)

    def __unicode__(self):
        return '%s on %s (Team %d) [GID: %d]' % (self.summoner_id.name, self.champion_id, self.team_id, self.game_id)

    def create_date_str(self):
        """Convert create_date epoch milliseconds timestamp to human-readable date string."""
        return time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(self.create_date/1000))

    def win(self):
        return self.stats.win

    class Meta:
        """These fields, taken together, ensure no duplicates are created."""
        unique_together = ('region', 'game_id', 'summoner_id')


###########
# LEAGUES #
###########


class League(models.Model):
    """
    Maps to Riot API League DTO.
    """

    region = models.CharField(max_length=4)     # ex. na
    queue = models.CharField(max_length=32)     # ex. RANKED_SOLO_5x5
    name = models.CharField(max_length=32)      # ex. Orianna's Warlocks
    tier = models.CharField(max_length=12)      # ex. CHALLENGER

    def __unicode__(self):
        return '' + self.region + ' ' + self.queue + ' ' + self.name + ' ' + self.tier

    class Meta:
        unique_together = ('region', 'queue', 'name', 'tier')


class LeagueEntry(models.Model):
    """
    Maps to Riot API LeagueEntry DTO.

    Child of League model (many-to-one).

    A summoner ID can be filtered by with this model's manager to get their solo queue entry.
    """

    division = models.CharField(max_length=3)                 # ex. IV
    is_fresh_blood = models.BooleanField()
    is_hot_streak = models.BooleanField()
    is_inactive = models.BooleanField()
    is_veteran = models.BooleanField()
    league_points = models.IntegerField()
    player_or_team_id = models.CharField(max_length=64)     # ex. TEAM-68594bb0-cce0-11e3-a7cc-782bcb4d1861
    player_or_team_name = models.CharField(max_length=24)   # ex. Smiteless Baron
    wins = models.IntegerField()

    # MiniSeries DTO
    series_losses = models.SmallIntegerField(null=True, blank=True)
    series_progress = models.CharField(null=True, blank=True, max_length=5)            # ex. WLLNN
    series_target = models.SmallIntegerField(null=True, blank=True)    # 2 or 3
    series_wins = models.SmallIntegerField(null=True, blank=True)

    league = models.ForeignKey(League)

    def __unicode__(self):
        return '' + self.league.__unicode__() + ' ' + self.division + ' - ' + self.player_or_team_name + ' (' + str(self.league_points) + ')'

    class Meta:
        unique_together = ('player_or_team_id', 'league')


#########
# TEAMS #
#########


class Team(models.Model):
    """
    Maps to Riot API Team DTO.

    To get Teams, given a summoner ID and region:
    Team.objects.filter(region=<region>).filter(roster__teammemberinfo__player_id=<summoner_id>)

    To get a LeagueEntry, given a team's full ID and region:
    LeagueEntry.objects.filter(league__region=<region>).get(player_or_team_id=<full_id>)
    """
    create_date = models.BigIntegerField()
    full_id = models.CharField(max_length=64)           # ex. TEAM-68594bb0-cce0-11e3-a7cc-782bcb4d1861
    last_game_date = models.BigIntegerField(null=True, blank=True)
    last_joined_ranked_team_queue_date = models.BigIntegerField()
    modify_date = models.BigIntegerField()
    name = models.CharField(max_length=24)
    last_join_date = models.BigIntegerField()           # date that the last member joined
    second_last_join_date = models.BigIntegerField()
    third_last_join_date = models.BigIntegerField()
    status = models.CharField(max_length=16)            # ex. RANKED
    tag = models.CharField(max_length=6)                # ex. TSM
    roster = models.OneToOneField('Roster')
    region = models.CharField(max_length=4)

    def create_date_str(self):
        """Convert create_date epoch milliseconds timestamp to human-readable date string."""
        return time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(self.create_date/1000))

    def last_game_date_str(self):
        """Convert last_game_date epoch milliseconds timestamp to human-readable date string."""
        if self.last_game_date is not None:
            return time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(self.last_game_date/1000))
        else:
            return -1

    def last_joined_ranked_team_queue_date_str(self):
        """Convert last_joined_ranked_team_queue_date epoch milliseconds timestamp to human-readable date string."""
        return time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(self.last_joined_ranked_team_queue_date/1000))

    def modify_date_str(self):
        """Convert modify_date epoch milliseconds timestamp to human-readable date string."""
        return time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(self.modify_date/1000))

    def last_join_date_str(self):
        """Convert last_join_date epoch milliseconds timestamp to human-readable date string."""
        if self.last_game_date is not None:
            return time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(self.last_game_date/1000))
        else:
            return -1

    def second_last_join_date_str(self):
        """Convert second_last_join_date epoch milliseconds timestamp to human-readable date string."""
        return time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(self.second_last_join_date/1000))

    def third_last_join_date_str(self):
        """Convert third_last_join_date epoch milliseconds timestamp to human-readable date string."""
        return time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(self.third_last_join_date/1000))

    def get_league_entries(self):
        """Returns the LeagueEntries for this Team, or None if the LeagueEntry does not exist."""
        try:
            obj = LeagueEntry.objects.filter(league__region=self.region).filter(player_or_team_id=self.full_id)
        except ObjectDoesNotExist:
            obj = None

        return obj

    def get_team_stat_detail(self):
        """Returns the TeamStatDetail for this Team."""
        queryset = TeamStatDetail.objects.filter(team=self)
        return queryset

    def __unicode__(self):
        return '' + self.name

    class Meta:
        # Prevent duplicate teams.
        unique_together = ('region', 'full_id')


class MatchHistorySummary(models.Model):
    """
    Maps to Riot API MatchHistorySummary DTO.

    Child of Team model (many-to-one).
    This will not be created for a Team if the team had never played a game when it was queried.
    """
    assists = models.IntegerField()
    date = models.BigIntegerField()
    deaths = models.IntegerField()
    game_id = models.BigIntegerField()
    game_mode = models.CharField(max_length=16)
    invalid = models.BooleanField()
    kills = models.IntegerField()
    map_id = models.IntegerField()
    opposing_team_kills = models.IntegerField()
    opposing_team_name = models.CharField(max_length=24)
    win = models.BooleanField()
    team = models.ForeignKey(Team)

    def date_str(self):
        """Convert date epoch milliseconds timestamp to human-readable date string."""
        return time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(self.date/1000))

    def __unicode__(self):
        return 'History of ' + self.team.__unicode__()


class Roster(models.Model):
    """
    Maps to Riot API Roster DTO.

    Child of Team model (one-to-one).

    This is it's own model (instead of being part of the Team model) to mirror Riot's backend
    to ease any future revisions.
    """
    owner_id = models.BigIntegerField()

    def __unicode__(self):
        return 'Roster of ' + Team.objects.get(roster=self).__unicode__()

    def get_summoner(self):
        """Converts owner_id to Summoner object, if possible. Otherwise returns owner_id."""
        try:
            # Can we resolve our player_id to a summoner in the DB?
            obj = Summoner.objects.filter(region=self.team.region).get(summoner_id=self.owner_id)
            return obj
        except ObjectDoesNotExist:
            # We don't know about this summoner, so just return their summoner ID.
            return self.owner_id


class TeamMemberInfo(models.Model):
    """
    Maps to Riot API TeamMemberInfo DTO.

    Child of Roster model (many-to-one).

    Holds data for a single member of a team's roster.
    """
    invite_date = models.BigIntegerField()
    join_date = models.BigIntegerField()
    player_id = models.BigIntegerField()
    status = models.CharField(max_length=16)            # ex. MEMBER
    roster = models.ForeignKey(Roster)

    def invite_date_str(self):
        """Convert invite_date epoch milliseconds timestamp to human-readable date string."""
        return time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(self.invite_date/1000))

    def join_date_str(self):
        """Convert join_date epoch milliseconds timestamp to human-readable date string."""
        return time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(self.join_date/1000))

    def get_summoner(self):
        """Converts player_id to Summoner object, if possible. Otherwise returns player_id."""
        try:
            # Can we resolve our player_id to a summoner in the DB?
            obj = Summoner.objects.filter(region=self.roster.team.region).get(summoner_id=self.player_id)
            return obj
        except ObjectDoesNotExist:
            # We don't know about this summoner, so just return their summoner ID.
            return self.player_id


    # Commented out until we can be sure we have matching Summoner object to resolve player_id to.
    # def __unicode__(self):
    #     this_team = Team.objects.get(roster=self.roster)
    #     return u'Member: ' + Summoner.objects.filter(region=this_team.region).get(summoner_id=self.player_id)

    class Meta:
        # Prevent duplicate players on the roster.
        unique_together = ('player_id', 'roster')


class TeamStatDetail(models.Model):
    """
    Maps to Riot API TeamStatDetail DTO.

    Child of Team model (many-to-one).

    Contains the stats for the game types (5x5 or 3x3).
    As such, each Team will have 2 of these, even if they only play one game type.
    """
    team_stat_type = models.CharField(max_length=16)    # ex. RANKED_TEAM_5x5
    average_games_played = models.IntegerField()        # ??
    wins = models.IntegerField()
    losses = models.IntegerField()
    team = models.ForeignKey(Team)


#########
# STATS #
#########


class PlayerStat(models.Model):
    """
    Maps to Riot API PlayerStatsSummaryList DTO.

    Child of Summoner model (one-to-one).
    """
    summoner = models.OneToOneField(Summoner)

    def __unicode__(self):
        return 'PlayerStat for ' + self.summoner.name

class PlayerStatsSummary(models.Model):
    """
    Maps to Riot API PlayerStatsSummary DTO.

    Child of PlayerStat model (many-to-one).
    """
    player = models.ForeignKey(PlayerStat)
    losses = models.IntegerField(blank=True, null=True)      # Ranked queue types only.
    wins = models.IntegerField()
    modify_date = models.BigIntegerField()                   # Date stats were last modified as epcoh ms.
    player_stat_summary_type = models.CharField(max_length=16)

    def get_aggregated_stat(self):
        return AggregatedStat.objects.get(player_stats=self)

    def modify_date_str(self):
        return time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(self.modify_date/1000))

    def __unicode__(self):
        return 'StatsSummary for ' + self.player.__unicode__()

class AggregatedStat(models.Model):
    """
    Maps to Riot API AggregatedStats DTO.

    Child of PlayerStatsSummary model (one-to-one).
    """
    player_stats = models.OneToOneField(PlayerStatsSummary)
    average_assists = models.IntegerField(null=True, blank=True)
    average_champions_killed = models.IntegerField(null=True, blank=True)
    average_combat_player_score = models.IntegerField(null=True, blank=True)
    average_node_capture = models.IntegerField(null=True, blank=True)
    average_node_capture_assist = models.IntegerField(null=True, blank=True)
    average_node_neutralize = models.IntegerField(null=True, blank=True)
    average_node_neutralize_assist = models.IntegerField(null=True, blank=True)
    average_num_deaths = models.IntegerField(null=True, blank=True)
    average_objective_player_score = models.IntegerField(null=True, blank=True)
    average_team_objective = models.IntegerField(null=True, blank=True)
    average_total_player_score = models.IntegerField(null=True, blank=True)
    bot_games_played = models.IntegerField(null=True, blank=True)
    killing_spree = models.IntegerField(null=True, blank=True)
    max_assists = models.IntegerField(null=True, blank=True)
    max_champions_killed = models.IntegerField(null=True, blank=True)
    max_combat_player_score = models.IntegerField(null=True, blank=True)
    max_largest_critical_strike = models.IntegerField(null=True, blank=True)
    max_largest_killing_spree = models.IntegerField(null=True, blank=True)
    max_node_capture = models.IntegerField(null=True, blank=True)
    max_node_capture_assist = models.IntegerField(null=True, blank=True)
    max_node_neutralize = models.IntegerField(null=True, blank=True)
    max_node_neutralize_assist = models.IntegerField(null=True, blank=True)
    max_num_deaths = models.IntegerField(null=True, blank=True)
    max_objective_player_score = models.IntegerField(null=True, blank=True)
    max_team_objective = models.IntegerField(null=True, blank=True)
    max_time_played = models.IntegerField(null=True, blank=True)
    max_time_spent_living = models.IntegerField(null=True, blank=True)
    max_total_player_score = models.IntegerField(null=True, blank=True)
    most_champion_kills_per_session = models.IntegerField(null=True, blank=True)
    most_spells_cast = models.IntegerField(null=True, blank=True)
    normal_games_played = models.IntegerField(null=True, blank=True)
    ranked_premade_games_played = models.IntegerField(null=True, blank=True)
    ranked_solo_games_played = models.IntegerField(null=True, blank=True)
    total_assists = models.IntegerField(null=True, blank=True)
    total_champion_kills = models.IntegerField(null=True, blank=True)
    total_damage_dealt = models.IntegerField(null=True, blank=True)
    total_damage_taken = models.IntegerField(null=True, blank=True)
    total_deaths_per_session = models.IntegerField(null=True, blank=True)
    total_double_kills = models.IntegerField(null=True, blank=True)
    total_first_blood = models.IntegerField(null=True, blank=True)
    total_gold_earned = models.IntegerField(null=True, blank=True)
    total_heal = models.IntegerField(null=True, blank=True)
    total_magic_damage_dealt = models.IntegerField(null=True, blank=True)
    total_minion_kills = models.IntegerField(null=True, blank=True)
    total_neutral_minions_killed = models.IntegerField(null=True, blank=True)
    total_node_capture = models.IntegerField(null=True, blank=True)
    total_node_neutralize = models.IntegerField(null=True, blank=True)
    total_penta_kills = models.IntegerField(null=True, blank=True)
    total_physical_damage_dealt = models.IntegerField(null=True, blank=True)
    total_quadra_kills = models.IntegerField(null=True, blank=True)
    total_sessions_lost = models.IntegerField(null=True, blank=True)
    total_sessions_played = models.IntegerField(null=True, blank=True)
    total_sessions_won = models.IntegerField(null=True, blank=True)
    total_triple_kills = models.IntegerField(null=True, blank=True)
    total_turrets_killed = models.IntegerField(null=True, blank=True)
    total_unreal_kills = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return 'AggStats for ' + self.player_stats.player.summoner.name + \
               '[' + self.player_stats.player_stat_summary_type + ']'
