from django.db import models

# Create your models here.

class Summoner(models.Model):
    summoner_id = models.BigIntegerField()
    name = models.CharField(max_length=16)
    profile_icon_id = models.IntegerField()
    revision_date = models.BigIntegerField()
    summoner_level = models.IntegerField()  # 'long' in DTO, but we know it's <= 30
    region = models.CharField(max_length=4)
    last_update = models.DateTimeField()

    def __str__(self):
        return u'{str.name}'.format(str=self)

class Champion(models.Model):
    champion_id = models.IntegerField()
    title = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    key = models.CharField(max_length=32)

    def __str__(self):
        return u'{str.name}'.format(str=self)

class Item(models.Model):
    item_id = models.IntegerField()
    description = models.CharField(max_length=1024)
    name = models.CharField(max_length=32)
    plain_text = models.CharField(max_length=256, blank=True, null=True)
    group = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return u'{str.name}'.format(str=self)

class SummonerSpell(models.Model):
    spell_id = models.IntegerField()
    summoner_level = models.IntegerField()
    name = models.CharField(max_length=16)
    key = models.CharField(max_length=32)
    description = models.CharField(max_length=256)

    def __str__(self):
        return u'{str.name}'.format(str=self)

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

#
# Following 3 hold recent matches data (see RecentGamesDto on API ref)
#

class Player(models.Model):
    champion = models.ForeignKey(Champion)
    summoner = models.ForeignKey(Summoner)
    team_id = models.IntegerField()  # 100, 200
    participant = models.ForeignKey('Game')

    def __str__(self):
        return u'{str.summoner} on {str.champion} (Team {str.team_id})'.format(str=self)

class RawStat(models.Model):
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

    def __str__(self):
        return u'Stats for {}'.format(Game.objects.get(stats=self))

    def __iter__(self):
        for i in self._meta.get_all_field_names():
            yield (i, getattr(self, i))

# FellowPlayer instances point to this to allow reverse-querying of participants
class Game(models.Model):
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

    def __str__(self):
        return u'{str.summoner_id.name} on {str.champion_id} (Team {str.team_id}) [GID: {str.game_id}]'.format(str=self)